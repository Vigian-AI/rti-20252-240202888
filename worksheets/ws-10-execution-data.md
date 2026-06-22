# WS-10: Experiment Execution & Data Collection

> **Bab 10 — Eksekusi Eksperimen & Pengumpulan Data**

---

## Ringkasan Materi

### Experiment Execution Pipeline

```
Design → Execution Plan → Controlled Execution → Data Collection → Data Logging → Dataset for Analysis
```

### Multiple Run = Non-Negotiable

Single run **tidak pernah cukup** untuk klaim ilmiah. Minimum 5-10 run per skenario dengan seed berbeda. Multiple run menghasilkan:
- Mean, std, confidence interval
- Distribusi hasil → uji statistik
- Variabilitas → error bar di grafik

### Execution Plan

Setiap eksperimen harus memiliki plan sebelum eksekusi:
- Daftar skenario
- Jumlah run per skenario
- Random seed per run (pre-determined!)
- Urutan eksekusi (randomisasi/counterbalancing)
- Pre-execution checklist

### Data Logging Komprehensif

Setiap run menghasilkan log terstruktur:
1. **Identitas** — Run ID, timestamp, skenario
2. **Konfigurasi** — Semua parameter, seed, code version
3. **Hasil** — Semua metrik, output detail
4. **Metadata** — Waktu eksekusi, resource usage, warning/error

Format: CSV/JSON/database — **bukan stdout yang di-copy-paste**.

### Engineering vs Research Execution

| Aspek | Engineering | Research |
|-------|-----------|---------|
| Run | Sekali (deploy) | Multiple (min 5-10, seed berbeda) |
| Logging | Error log, access log | Semua parameter, metrik, metadata |
| Anomali | Bug → fix → redeploy | Investigasi → dokumentasi → analisis |
| Urutan | Tidak penting | Bisa bias — perlu randomisasi |

### Anomali = Dokumentasi, Bukan Hapus

Run gagal/anomali tidak boleh dihapus tanpa dokumentasi. Bisa jadi:
- **Bug** → fix & re-run (dokumentasikan!)
- **Batas kemampuan metode** → DNF = temuan
- **Data yang bias** jika hanya simpan run "berhasil"

### Jebakan Kognitif

1. "Satu angka cukup" → tanpa distribusi, tidak bisa diuji
2. "Seed tidak penting" → bahkan algoritma deterministik bisa dipengaruhi library stokastik
3. "Run gagal langsung hapus" → kehilangan temuan potensial
4. "Semua run harus hari ini" → thermal throttling, fatigue

---

## Template A.10 — Execution Plan & Data Log

```
EXECUTION PLAN

| Run # | Skenario | Seed | Parameter | Status | Waktu | Output File |
|-------|----------|------|-----------|--------|-------|-------------|
| 1     |          |      |           |        |       |             |
| 2     |          |      |           |        |       |             |
| 3     |          |      |           |        |       |             |
| ...   |          |      |           |        |       |             |

Jumlah runs per skenario : ____
Total runs               : ____

DATA LOG (per run):
  Run ID    : ____________________
  Timestamp : ____________________
  Skenario  : ____________________
  Input     : ____________________
  Output    : ____________________
  Anomali   : ____________________
  Catatan   : ____________________
```

---

## Latihan 1 — Execution Plan

Execution plan eksperimen perbandingan Spring Boot vs .NET pada MongoDB. Seed ditentukan sebelum eksekusi; urutan run diacak (counterbalancing) agar tidak semua run Spring Boot lebih dulu.

**Pre-execution checklist (wajib dipenuhi sebelum Run #1):**
- [ ] `docker compose build` berhasil tanpa error
- [ ] Dataset IKEA Product Catalog (401.046 dokumen dari `IKEA_product_catalog.csv`) sudah ter-import ke MongoDB
- [ ] Verifikasi kedua API merespons (`GET /health`) sebelum k6 dijalankan
- [ ] Resource limit container terkunci di `docker-compose.yml` (cpus=2, memory=2g)
- [ ] Background process host dimatikan (Windows Update, OneDrive sync)
- [ ] `experiment-config.yaml` sudah di-commit ke version control

| Run # | Skenario | Seed (dataset) | Parameter Kunci | Urutan Eksekusi | Status |
|-------|----------|---------------|----------------|-----------------|--------|
| 1  | Spring Boot — CRUD MongoDB | N/A (data riil) | VU=50, ramp=30s, steady=120s, warmup=30s | 1 | Planned |
| 2  | .NET — CRUD MongoDB        | N/A (data riil) | VU=50, ramp=30s, steady=120s, warmup=30s | 2 | Planned |
| 3  | .NET — CRUD MongoDB        | N/A (data riil) | VU=50, ramp=30s, steady=120s, warmup=30s | 3 | Planned |
| 4  | Spring Boot — CRUD MongoDB | N/A (data riil) | VU=50, ramp=30s, steady=120s, warmup=30s | 4 | Planned |
| 5  | Spring Boot — CRUD MongoDB | N/A (data riil) | VU=50, ramp=30s, steady=120s, warmup=30s | 5 | Planned |
| 6  | .NET — CRUD MongoDB        | N/A (data riil) | VU=50, ramp=30s, steady=120s, warmup=30s | 6 | Planned |
| 7  | .NET — CRUD MongoDB        | N/A (data riil) | VU=50, ramp=30s, steady=120s, warmup=30s | 7 | Planned |
| 8  | Spring Boot — CRUD MongoDB | N/A (data riil) | VU=50, ramp=30s, steady=120s, warmup=30s | 8 | Planned |
| 9  | Spring Boot — CRUD MongoDB | N/A (data riil) | VU=50, ramp=30s, steady=120s, warmup=30s | 9 | Planned |
| 10 | .NET — CRUD MongoDB        | N/A (data riil) | VU=50, ramp=30s, steady=120s, warmup=30s | 10 | Planned |

> **Catatan urutan:** Run diinterleave (SB–DN–DN–SB–SB–DN–DN–SB–SB–DN) untuk mencegah bias urutan. Container di-recreate (`docker compose down -v`) sebelum setiap run untuk reset JVM dan cache state.
>
> **Catatan dataset:** Dataset yang digunakan adalah `IKEA_product_catalog.csv` (401.046 baris, 18 kolom: `unique_id`, `product_id`, `product_name`, `product_type`, `product_measurements`, `product_description`, `main_category`, `sub_category`, `product_rating`, `product_rating_count`, `badge`, `online_sellable`, `url`, `price`, `currency`, `discount`, `sale_tag`, `country`). Data di-import sekali ke MongoDB sebelum eksperimen dimulai dan tidak diubah antar-run — konsistensi data dijamin karena sumber adalah file CSV yang di-commit ke version control.

**Total skenario:** 2 (Spring Boot, .NET)
**Run per skenario:** 5
**Total run keseluruhan:** 10

---

## Latihan 2 — Data Log Terstruktur

Format data log untuk setiap run eksperimen. Semua field dicatat otomatis oleh k6 (`--out json`) dan metadata tambahan dari skrip `run_experiment.py`.

**Identitas:**
| Field | Contoh |
|-------|--------|
| Run ID | `sb-run-003` / `dn-run-002` |
| Timestamp (start) | `2026-06-22T10:00:00Z` |
| Timestamp (end) | `2026-06-22T10:03:20Z` |
| Skenario | `spring-boot` / `dotnet` |

**Konfigurasi:**
| Field | Contoh |
|-------|--------|
| Dataset source | `IKEA_product_catalog.csv` (di-commit ke version control, di-mount ke container data-importer) |
| Dataset size | 401.046 dokumen, 18 field per dokumen |
| MongoDB collection | `ikea_products` |
| MongoDB URI | `mongodb://mongodb:27017/benchmark_db` |
| Virtual users | `50` |
| Ramp-up duration | `30s` |
| Steady-state window | `120s` |
| Warmup duration | `30s` (dikecualikan dari pengukuran) |
| MongoDB URI | `mongodb://mongodb:27017/benchmark_db` |
| Docker image (API) | `eclipse-temurin:21-jre-alpine` / `mcr.microsoft.com/dotnet/aspnet:8.0-alpine` |
| Docker image (MongoDB) | `mongo:7.0` |
| k6 image | `grafana/k6:0.51.0` |
| Container CPU limit | `2` |
| Container memory limit | `2g` |
| Config file hash | `sha256:a1b2c3...` (hash dari `experiment-config.yaml`) |
| Git commit | `abc1234` |

**Hasil (metrik primary dan secondary):**
| Metrik | Tipe Data | Satuan | Range Valid |
|--------|----------|--------|-------------|
| throughput_rps | float | requests/sec | > 0 |
| p95_latency_ms | float | ms | > 0 |
| p99_latency_ms | float | ms | > p95_latency_ms |
| error_rate_pct | float | % | 0.0 – 100.0 |
| iterations_total | int | — | > 0 |
| data_received_mb | float | MB | > 0 |
| data_sent_mb | float | MB | > 0 |

**Format output:** [ ] CSV / [ ] JSON / [ ] Database / [ ] Lainnya

> CSV dipilih karena langsung bisa dibuka di spreadsheet untuk inspeksi manual, dan mudah di-load ke pandas/R untuk analisis statistik tanpa parsing tambahan. Setiap run menghasilkan satu baris di file CSV agregat `results/all_runs.csv`.

**Contoh output agregat (`results/all_runs.csv`):**
```
run_id,scenario,timestamp_start,timestamp_end,dataset_source,dataset_rows,dataset_sha256,virtual_users,ramp_up,steady_state,warmup,docker_image,mongo_image,git_commit,throughput_rps,p95_latency_ms,p99_latency_ms,error_rate_pct,iterations_total,data_received_mb,data_sent_mb,anomaly
sb-run-001,spring-boot,2026-06-22T10:00:00Z,2026-06-22T10:03:20Z,IKEA_product_catalog.csv,401046,abc123...,50,30s,120s,30s,eclipse-temurin:21-jre-alpine,mongo:7.0,abc1234,1250.4,48.7,72.1,0.0,150048,42.3,18.7,
dn-run-001,dotnet,2026-06-22T10:05:00Z,2026-06-22T10:08:20Z,IKEA_product_catalog.csv,401046,abc123...,50,30s,120s,30s,mcr.microsoft.com/dotnet/aspnet:8.0-alpine,mongo:7.0,abc1234,1310.2,44.1,68.5,0.0,157224,44.1,19.3,
```

---

## Latihan 3 — Anomaly Protocol

Protokol penanganan anomali untuk eksperimen benchmarking ini.

| Jenis Anomali | Contoh Konkret | Tindakan |
|---------------|---------------|----------|
| Run gagal (crash) | Container API crash di tengah k6 run karena OOM atau port conflict | 1. Catat run_id, timestamp, dan error log container. 2. Jangan hapus output parsial — simpan sebagai `*-FAILED.json`. 3. Investigasi penyebab (cek `docker logs`). 4. Perbaiki jika bug, lalu re-run dengan run_id baru dan catat perubahan yang dilakukan. |
| Hasil ekstrem (outlier) | Throughput turun >50% dibanding run lain pada skenario yang sama | 1. Dokumentasikan nilai anomali di field `anomaly` pada JSON. 2. Periksa apakah ada background process host atau thermal throttling. 3. Jangan langsung hapus — laporkan sebagai outlier dan analisis dengan/tanpa outlier tersebut. |
| Waktu eksekusi anomali | Run selesai 2x lebih lambat dari biasanya (mis. 6 menit vs 3 menit normal) | 1. Catat durasi aktual di log. 2. Cek apakah container di-recreate dengan benar sebelum run (JVM/cache state). 3. Jika penyebab tidak bisa dikontrol (host sleep mode), eksklusi run dengan justifikasi tertulis. |
| Inkonsistensi antar-run | p95 latency satu run = 180ms, sementara 4 run lain berkisar 45-55ms | 1. Tandai sebagai outlier dengan metode IQR (di luar Q1−1.5×IQR atau Q3+1.5×IQR). 2. Laporkan analisis dengan dan tanpa outlier. 3. Investigasi apakah container sudah di-recreate dan apakah warmup sudah dijalankan sebelum window pengukuran. |

**Prinsip:** Detect → Investigate → Document → Decide

> **Threshold anomali otomatis** yang akan diimplementasi di `analyze.py`: jika nilai metrik suatu run menyimpang lebih dari 3× standard deviation dari mean skenario yang sama, run tersebut otomatis diflag sebagai outlier kandidat dan disertakan dalam laporan untuk keputusan manual.

---

## Refleksi

> Pernahkah Anda melaporkan hasil riset/tugas dari single run? Apa risikonya? Bagaimana multiple run mengubah kepercayaan terhadap hasil?

**Pengalaman sebelumnya:**
> Ya — dalam tugas pengujian performa sebelumnya, pernah menjalankan satu kali benchmark dan langsung menggunakan angka tersebut sebagai hasil. Pada waktu itu angka terlihat meyakinkan karena tidak ada perbandingan, sehingga tidak terlihat bahwa hasil itu mungkin tidak representatif.

**Yang akan dilakukan berbeda:**
> Dengan 5 run per skenario (total 10 run untuk dua framework), setiap angka yang dilaporkan adalah rata-rata dengan standard deviation dan confidence interval — bukan satu titik data. Ini mengubah klaim dari "Spring Boot menghasilkan 1250 RPS" menjadi "Spring Boot menghasilkan rata-rata 1248 ± 32 RPS (95% CI: 1210–1286)", yang jauh lebih jujur dan bisa diuji secara statistik. Selain itu, adanya distribusi memungkinkan deteksi outlier dan pengujian normalitas sebelum memilih uji statistik yang tepat (t-test vs Mann-Whitney U).
