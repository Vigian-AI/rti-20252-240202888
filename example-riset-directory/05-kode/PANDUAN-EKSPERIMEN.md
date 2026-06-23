# Panduan Eksperimen: Spring Boot vs .NET pada MongoDB

> Panduan lengkap dari persiapan awal hingga data siap digunakan untuk penulisan jurnal.
> Ikuti urutan tahap ini secara berurutan.

---

## Prasyarat

Pastikan software berikut sudah terinstall di host (Windows 11):

| Software | Versi minimum | Cek |
|----------|--------------|-----|
| Docker Desktop | 29.x | `docker --version` |
| Git | 2.x | `git --version` |

Docker Desktop harus dalam kondisi **running** sebelum memulai.

---

## Tahap 0 — Persiapan Satu Kali

Tahap ini hanya dilakukan sekali di awal, tidak perlu diulang setiap eksperimen.

### 0.1 Clone repositori

```bash
git clone <url-repo>
cd rti-20252-240202888
```

### 0.2 Konfigurasi WSL2 (penting untuk stabilitas benchmark)

Buat file `.wslconfig` di `C:\Users\<username>\` untuk membatasi resource WSL2
agar tidak bersaing dengan proses host saat benchmark berjalan:

```ini
# C:\Users\Vg_\.wslconfig
[wsl2]
memory=12GB
processors=6
swap=0
```

> Setelah menyimpan file ini, restart WSL2:
> ```
> wsl --shutdown
> ```
> Lalu buka kembali Docker Desktop.

### 0.3 Build Docker image

```bash
cd example-riset-directory/05-kode

docker compose build
```

Proses ini mengunduh base image dan mengkompilasi kedua aplikasi.
Bisa memakan waktu 5–15 menit tergantung koneksi internet.
Cukup dilakukan **sekali** — kecuali ada perubahan kode.

### 0.4 Verifikasi SHA-256 file CSV

Catat hash file dataset untuk keperluan dokumentasi reproducibility:

```bash
# Windows PowerShell
Get-FileHash ..\04-data\IKEA_product_catalog.csv -Algorithm SHA256
```

Simpan nilai hash ini. Nanti dimasukkan ke kolom `dataset_sha256` di hasil CSV.

### 0.5 Import dataset ke MongoDB

Langkah ini menjalankan MongoDB, mengimpor 401.046 dokumen dari CSV,
lalu **membiarkan MongoDB tetap berjalan** untuk semua run berikutnya.

```bash
# Nyalakan MongoDB
docker compose up -d mongodb

# Tunggu MongoDB sehat (biasanya 10-15 detik)
docker compose ps
# STATUS kolom mongodb harus: healthy

# Import data CSV → koleksi ikea_products
docker compose --profile import up data-importer
```

Tunggu hingga muncul pesan seperti:
```
[DONE] 401,046 dokumen diimpor, 0 dilewati (duplikat) dalam 85.3s
```

Verifikasi data masuk:

```bash
docker compose exec mongodb mongosh benchmark_db --eval "db.ikea_products.countDocuments()"
# Output yang diharapkan: 401046
```

> Data hanya perlu diimpor **sekali**. MongoDB menggunakan Docker volume `mongo-data`
> sehingga data tetap ada selama volume tidak di-hapus.

---

## Tahap 1 — Pre-Execution Checklist

Sebelum setiap sesi benchmarking (bisa lebih dari satu hari),
pastikan semua kondisi ini terpenuhi:

- [ ] Docker Desktop dalam kondisi running
- [ ] Tidak ada Windows Update yang berjalan (`Settings > Windows Update > Pause`)
- [ ] OneDrive sync di-pause (klik kanan ikon OneDrive di taskbar → Pause sync)
- [ ] Tidak ada download/upload besar yang berjalan
- [ ] Laptop terhubung ke charger (bukan mode battery saver)
- [ ] MongoDB masih berjalan dan data sudah ada:
  ```bash
  docker compose exec mongodb mongosh benchmark_db \
    --eval "db.ikea_products.countDocuments()"
  # Harus: 401046
  ```

---

## Tahap 2 — Eksekusi Benchmark

Lakukan **10 run total**: 5 untuk Spring Boot, 5 untuk .NET,
dengan urutan interleave agar tidak ada bias urutan.

Urutan yang sudah ditentukan (wajib diikuti):

```
Run 1 : Spring Boot
Run 2 : .NET
Run 3 : .NET
Run 4 : Spring Boot
Run 5 : Spring Boot
Run 6 : .NET
Run 7 : .NET
Run 8 : Spring Boot
Run 9 : Spring Boot
Run 10: .NET
```

Buat folder hasil jika belum ada:

```bash
mkdir -p results
```

---

### Prosedur satu run (ulangi untuk Run 1 sampai Run 10)

> Ganti `<FRAMEWORK>`, `<TARGET>`, dan `<FILENAME>` sesuai tabel di bawah.

**Langkah A — Nyalakan API yang akan diuji**

Untuk Spring Boot:
```bash
docker compose --profile springboot up -d springboot-api

# Tunggu hingga status healthy
docker compose ps
# springboot-api harus: healthy
```
docker compose --profile k6 run --rm k6 run /scripts/load-test.js `
  -e TARGET=http://springboot-api:8080 `
  --out csv=/results/sb-run-001.csv

Untuk .NET:
```bash
docker compose --profile dotnet up -d dotnet-api

# Tunggu hingga status healthy
docker compose ps
# dotnet-api harus: healthy
```

**Langkah B — Verifikasi API merespons**

```bash
# Spring Boot
curl http://localhost:8080/actuator/health

# .NET
curl http://localhost:5000/health
```

Kedua endpoint harus mengembalikan status `UP` / `{"status":"UP"}`.

**Langkah C — Jalankan k6**

```bash
docker compose --profile k6 run --rm k6 run /scripts/load-test.js \
  -e TARGET=<TARGET> \
  --out csv=/results/<FILENAME>
```

**Langkah D — Reset state (WAJIB sebelum run berikutnya)**

```bash
docker compose --profile springboot down
# atau
docker compose --profile dotnet down
```

> Jangan gunakan `-v` di sini agar data MongoDB tidak terhapus.
> Yang di-reset hanya container API-nya, bukan volume MongoDB.

---

### Tabel referensi 10 run

| Run | Framework | `<TARGET>` | `<FILENAME>` |
|-----|-----------|-----------|--------------|
| 1 | Spring Boot | `http://springboot-api:8080` | `sb-run-001.csv` |
| 2 | .NET | `http://dotnet-api:5000` | `dn-run-001.csv` |
| 3 | .NET | `http://dotnet-api:5000` | `dn-run-002.csv` |
| 4 | Spring Boot | `http://springboot-api:8080` | `sb-run-002.csv` |
| 5 | Spring Boot | `http://springboot-api:8080` | `sb-run-003.csv` |
| 6 | .NET | `http://dotnet-api:5000` | `dn-run-003.csv` |
| 7 | .NET | `http://dotnet-api:5000` | `dn-run-004.csv` |
| 8 | Spring Boot | `http://springboot-api:8080` | `sb-run-004.csv` |
| 9 | Spring Boot | `http://springboot-api:8080` | `sb-run-005.csv` |
| 10 | .NET | `http://dotnet-api:5000` | `dn-run-005.csv` |

Setelah semua 10 run selesai, folder `results/` harus berisi 10 file CSV:

```
results/
├── sb-run-001.csv
├── sb-run-002.csv
├── sb-run-003.csv
├── sb-run-004.csv
├── sb-run-005.csv
├── dn-run-001.csv
├── dn-run-002.csv
├── dn-run-003.csv
├── dn-run-004.csv
└── dn-run-005.csv
```

---

## Tahap 3 — Ekstraksi Metrik dari Output k6

k6 dengan `--out csv` menghasilkan baris per request mentah.
Kita perlu mengekstrak metrik agregat (RPS, p95, p99, error rate) dari setiap file CSV.

Buat skrip `scripts/extract_metrics.py`:

```python
"""
extract_metrics.py
Ekstrak metrik agregat dari output CSV k6 dan gabungkan ke all_runs.csv.

Usage:
    python extract_metrics.py --input results/ --output results/all_runs.csv
"""

import argparse
import csv
import os
import numpy as np
from pathlib import Path


def extract(filepath: Path) -> dict:
    """Baca satu file CSV k6 dan hitung metrik agregat."""
    filename = filepath.stem          # misal: sb-run-001
    scenario = "spring-boot" if filename.startswith("sb") else "dotnet"
    run_num  = filename.split("-")[-1]  # 001, 002, dst

    durations = []   # http_req_duration dalam ms (window steady-state)
    errors    = 0
    total     = 0

    with open(filepath, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            metric = row.get("metric_name", "")
            if metric == "http_req_duration":
                try:
                    durations.append(float(row["metric_value"]))
                    total += 1
                except ValueError:
                    pass
            elif metric == "http_req_failed":
                try:
                    errors += float(row["metric_value"])
                except ValueError:
                    pass

    if not durations:
        return {}

    arr = np.array(durations)
    # RPS: total request / durasi steady-state (120 detik)
    rps = round(total / 120, 2)

    return {
        "run_id":           filename,
        "scenario":         scenario,
        "throughput_rps":   rps,
        "p95_latency_ms":   round(float(np.percentile(arr, 95)), 2),
        "p99_latency_ms":   round(float(np.percentile(arr, 99)), 2),
        "mean_latency_ms":  round(float(np.mean(arr)), 2),
        "error_rate_pct":   round((errors / total) * 100, 4) if total > 0 else 0.0,
        "iterations_total": total,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input",  required=True, help="Folder berisi file CSV k6")
    parser.add_argument("--output", required=True, help="Path output all_runs.csv")
    args = parser.parse_args()

    results_dir = Path(args.input)
    csv_files   = sorted(results_dir.glob("*.csv"))

    rows = []
    for f in csv_files:
        if f.name == "all_runs.csv":
            continue
        print(f"  Memproses {f.name} ...")
        row = extract(f)
        if row:
            rows.append(row)

    if not rows:
        print("[ERROR] Tidak ada data ditemukan.")
        return

    fieldnames = list(rows[0].keys())
    with open(args.output, "w", newline="", encoding="utf-8") as out:
        writer = csv.DictWriter(out, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"\n[DONE] {len(rows)} run ditulis ke {args.output}")


if __name__ == "__main__":
    main()
```

Jalankan ekstraksi:

```bash
docker compose run --rm -v "$(pwd)/results:/results" -v "$(pwd)/scripts:/scripts" \
  python:3.12-alpine sh -c \
  "pip install numpy --quiet && python /scripts/extract_metrics.py \
   --input /results --output /results/all_runs.csv"
```

Atau di PowerShell (Windows):

```powershell
docker run --rm `
  -v "${PWD}\results:/results" `
  -v "${PWD}\scripts:/scripts" `
  python:3.12-alpine `
  sh -c "pip install numpy --quiet && python /scripts/extract_metrics.py --input /results --output /results/all_runs.csv"
```

---

## Tahap 4 — Analisis Statistik

File `results/all_runs.csv` sekarang berisi 10 baris (5 Spring Boot, 5 .NET).
Langkah analisis untuk mendapatkan angka yang bisa masuk jurnal:

### 4.1 Cek normalitas (Shapiro-Wilk)

```python
import pandas as pd
from scipy import stats

df = pd.read_csv("results/all_runs.csv")
sb = df[df["scenario"] == "spring-boot"]
dn = df[df["scenario"] == "dotnet"]

for metric in ["throughput_rps", "p95_latency_ms"]:
    _, p_sb = stats.shapiro(sb[metric])
    _, p_dn = stats.shapiro(dn[metric])
    print(f"{metric}: Spring Boot p={p_sb:.4f}, .NET p={p_dn:.4f}")
    print(f"  -> {'Normal' if p_sb > 0.05 and p_dn > 0.05 else 'Tidak normal — gunakan Mann-Whitney U'}")
```

### 4.2 Uji beda (t-test atau Mann-Whitney U)

```python
# Jika kedua distribusi normal → t-test
t_stat, p_val = stats.ttest_ind(sb["throughput_rps"], dn["throughput_rps"])

# Jika salah satu tidak normal → Mann-Whitney U
u_stat, p_val = stats.mannwhitneyu(sb["throughput_rps"], dn["throughput_rps"],
                                    alternative="two-sided")

print(f"p-value: {p_val:.4f}")
print(f"Signifikan (α=0.05): {'Ya' if p_val < 0.05 else 'Tidak'}")
```

### 4.3 Effect size (Cohen's d)

```python
def cohens_d(a, b):
    pooled_std = ((a.std(ddof=1)**2 + b.std(ddof=1)**2) / 2) ** 0.5
    return (a.mean() - b.mean()) / pooled_std

d = cohens_d(sb["throughput_rps"], dn["throughput_rps"])
print(f"Cohen's d: {d:.4f}")
# < 0.2 = kecil, 0.2-0.5 = sedang, > 0.5 = besar (threshold riset: ≥ 0.5)
```

### 4.4 Tabel ringkasan untuk jurnal

```python
summary = df.groupby("scenario")[["throughput_rps", "p95_latency_ms", "p99_latency_ms"]].agg(
    ["mean", "std", "min", "max"]
)
print(summary.round(2).to_string())
summary.to_csv("results/summary_stats.csv")
```

---

## Tahap 5 — Output Akhir yang Siap Jurnal

Setelah Tahap 4, tersedia file-file berikut di folder `results/`:

| File | Isi | Digunakan untuk |
|------|-----|----------------|
| `all_runs.csv` | 10 baris metrik per run | Raw data, lampiran jurnal |
| `summary_stats.csv` | Mean ± SD per framework | Tabel hasil di badan jurnal |
| (grafik manual) | Box plot / bar chart | Gambar/figure di jurnal |

### Angka minimum yang harus dilaporkan di jurnal

1. **Mean ± SD** throughput (RPS) untuk masing-masing framework
2. **Mean ± SD** p95 latency (ms) untuk masing-masing framework
3. **p-value** dari uji statistik (t-test atau Mann-Whitney U), dengan α = 0.05
4. **Effect size** Cohen's d (atau Cliff's delta jika non-parametrik)
5. **Nama uji** yang digunakan beserta justifikasi pemilihannya (hasil Shapiro-Wilk)

### Contoh kalimat hasil di jurnal

> "Spring Boot menghasilkan rata-rata throughput sebesar X ± Y RPS
> sedangkan .NET menghasilkan X' ± Y' RPS. Hasil uji [t-test / Mann-Whitney U]
> menunjukkan perbedaan yang [signifikan / tidak signifikan] secara statistik
> (p = 0.xxx, α = 0.05) dengan effect size Cohen's d = 0.xx
> yang tergolong [kecil / sedang / besar]."

---

## Referensi Cepat — Perintah Penting

```bash
# Cek status semua container
docker compose ps

# Lihat log container secara live
docker compose logs -f springboot-api
docker compose logs -f dotnet-api

# Stop semua container (tanpa hapus data)
docker compose down

# Hapus semua container DAN volume (reset total — hati-hati, data MongoDB hilang!)
docker compose down -v

# Rebuild image setelah perubahan kode
docker compose build --no-cache
```
