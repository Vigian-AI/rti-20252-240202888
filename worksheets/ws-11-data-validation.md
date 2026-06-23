# WS-11: Data Validation & Integrity

> **Bab 11 — Validasi Data & Integritas**

---

## Ringkasan Materi

### Data Trust Model

```
Raw Data → Data Cleaning → Consistency Check → Validation Process → Trusted Data
```

Data mentah belum bisa dipercaya. Harus melewati pipeline validasi sebelum siap untuk analisis statistik.

### Empat Pilar Data Quality

| Pilar | Deskripsi | Contoh Pelanggaran |
|-------|----------|-------------------|
| **Accuracy** | Nilai dalam range masuk akal | Akurasi = 1.5 (di luar [0,1]) |
| **Consistency** | Format seragam di semua run | Run 1: CSV, Run 2: JSON |
| **Completeness** | Tidak ada data hilang dari plan | 97 dari 100 run tercatat |
| **Validity** | Data sesuai desain eksperimen | Parameter baseline tercampur treatment |

### Proses Validasi Progresif

1. **Format validation** — Tipe file, header, kolom
2. **Range validation** — Nilai dalam batas logis
3. **Consistency validation** — Format seragam antar-run
4. **Logic validation** — Data cocok dengan desain eksperimen

Jika gagal di langkah awal → tidak perlu lanjut.

### Anomaly Detection — 3 Jenis

| Jenis | Deskripsi | Deteksi |
|-------|----------|---------|
| **Statistical outlier** | Nilai di luar distribusi normal | IQR: < Q1-1.5×IQR atau > Q3+1.5×IQR |
| **Contextual anomaly** | Normal absolut, abnormal dalam konteks | Run 1-10: ~91%, Run 11-20: ~88% |
| **Pattern anomaly** | Pola sistematis (bukan random) | Performa menurun berurutan |

**Prinsip:** Detect → Investigate → Document → Decide — **JANGAN langsung hapus.**

### Engineering vs Research Validation

| Aspek | Engineering | Research |
|-------|-----------|---------|
| Tujuan | Data sesuai spesifikasi bisnis | Data layak untuk analisis statistik |
| Missing data | Impute / set default | Investigasi penyebab → dokumentasi |
| Outlier | Bug → fix | Mungkin temuan → investigasi |
| Dokumentasi | Minimal (log error) | Komprehensif (anomali + keputusan) |

### Jebakan Kognitif

1. "Logging otomatis ≠ data benar" → bisa ada bug di logger
2. "Outlier = hapus" → bisa jadi temuan penting
3. "Dataset kecil tidak perlu validasi" → justru lebih rentan
4. "Mean normal = data benar" → [94, 95, 93, **44**, 94] → mean 84% terlihat wajar

---

## Template A.11 — Data Validation Checklist

```
DATA VALIDATION CHECKLIST

Completeness:
  [ ] Semua skenario tercakup
  [ ] Jumlah run sesuai rencana
  [ ] Tidak ada file output hilang
  Missing: ____ dari ____ data points

Format Consistency:
  [ ] Semua file format sama (CSV/JSON/...)
  [ ] Header konsisten
  [ ] Tipe data konsisten (numerik tetap numerik)

Range & Logic:
  [ ] Nilai dalam range masuk akal
  [ ] Tidak ada waktu negatif
  [ ] Metrik 0–100%, tidak di luar range
  Anomali ditemukan: ____________________

Cross-Validation:
  [ ] Run identik → hasil mendekati
  [ ] Trend konsisten dengan ekspektasi teori

Keputusan:
  [ ] Data siap analisis
  [ ] Perlu cleaning
  [ ] Perlu re-run (skenario: ____)
```

---

## Latihan 1 — Completeness Check

Status pengumpulan data per tanggal validasi ini (23 Juni 2026).
Run 1–4 sudah selesai, run 5–10 masih dalam proses pengambilan data.

| File | Skenario | Status | Jumlah Request | Catatan |
|------|----------|--------|----------------|---------|
| sb-run-001.csv | Spring Boot | ✅ Selesai | 2.904 | Valid |
| sb-run-002.csv | Spring Boot | ✅ Selesai | 2.948 | Valid |
| sb-run-003.csv | Spring Boot | ⏳ Belum | — | Menunggu eksekusi |
| sb-run-004.csv | Spring Boot | ⏳ Belum | — | Menunggu eksekusi |
| sb-run-005.csv | Spring Boot | ⏳ Belum | — | Menunggu eksekusi |
| dn-run-001.csv | .NET | ✅ Selesai | 27.176 | Valid, 3 POST 500 minor |
| dn-run-002.csv | .NET | ✅ Selesai | 27.142 | Valid |
| dn-run-003.csv | .NET | ⏳ Belum | — | Menunggu eksekusi |
| dn-run-004.csv | .NET | ⏳ Belum | — | Menunggu eksekusi |
| dn-run-005.csv | .NET | ⏳ Belum | — | Menunggu eksekusi |

**Total expected:** 10 run | **Total actual:** 4 run | **Missing:** 6 run

**Keputusan untuk data missing:**
> 6 run yang belum ada akan dieksekusi sesuai RUN-COMMANDS.md. Validasi final dilakukan setelah semua 10 run terkumpul. Analisis statistik (t-test / Mann-Whitney U) tidak bisa dilakukan sebelum seluruh data tersedia karena membutuhkan n=5 per kelompok.

---

## Latihan 2 — Anomaly Investigation

Validasi 4 run yang sudah terkumpul menggunakan data aktual dari `results/`.

### Data saat ini (metrik p95 latency per run)

| Run | Skenario | n requests | RPS | Mean (ms) | Std Dev (ms) | p95 (ms) | p99 (ms) |
|-----|----------|-----------|-----|-----------|-------------|----------|----------|
| sb-run-001 | Spring Boot | 2.904 | 24,2 | 867,3 | 933,8 | 2.296,7 | 2.696,5 |
| sb-run-002 | Spring Boot | 2.948 | 24,6 | 854,1 | 893,4 | 2.197,4 | 2.502,0 |
| dn-run-001 | .NET | 27.176 | 226,5 | 2,36 | 2,24 | 3,40 | 4,93 |
| dn-run-002 | .NET | 27.142 | 226,2 | 2,56 | 2,48 | 4,54 | 6,17 |

### Deteksi outlier antar-run (per skenario, metrik RPS)

**Spring Boot — RPS: [24,2 ; 24,6]** (hanya 2 run, belum bisa IQR — perlu minimal 4 titik)
> Kedua nilai sangat dekat (selisih 0,4 RPS = 1,6%) → konsistensi tinggi untuk data awal.

**.NET — RPS: [226,5 ; 226,2]** (hanya 2 run)
> Selisih 0,3 RPS = 0,13% → konsistensi sangat tinggi.

**Anomali yang terdeteksi:**

| Anomali | Nilai | Kemungkinan Penyebab | Keputusan |
|---------|-------|---------------------|-----------|
| dn-run-002: POST 500 (3 kasus) | 3 dari 4.199 POST = 0,07% | Kemungkinan race condition saat container baru naik, pool koneksi MongoDB belum penuh | Dapat diabaikan (< 0,1%) — dokumentasi saja, tidak perlu re-run |
| Spring Boot RPS sangat rendah vs .NET | SB: ~24 RPS vs DN: ~226 RPS (rasio 1:9,4) | JVM belum warm optimal dalam window 120s, atau container resource limit (2 CPU, 2GB) tidak cukup untuk Spring Boot dengan beban tinggi | Investigasi: jalankan warmup test tambahan, bandingkan dengan threshold teoritis literatur |
| Spring Boot std dev sangat besar | std=933 ms hampir setara mean=867 ms | Distribusi latency sangat skewed — ada request yang sangat lambat (max 3.305 ms) bersamaan dengan yang sangat cepat (min 0,21 ms) | Laporkan distribusi lengkap, gunakan median dan p95 sebagai metrik utama bukan mean |

### Konsistensi format

- [x] Semua 4 file berformat CSV
- [x] Header identik di semua file: `metric_name, timestamp, metric_value, check, error, error_code, expected_response, group, method, name, proto, scenario, service, status, subproto, tls_version, url, extra_tags, metadata`
- [x] Kolom `metric_value` bertipe float di semua file
- [x] Kolom `status` bertipe string integer (200, 201, 204, 404, 500)
- [x] Tidak ada nilai negatif pada `metric_value` untuk `http_req_duration`
- [x] Tidak ada baris dengan `metric_name = http_req_duration` yang memiliki `metric_value = 0`

---

## Latihan 3 — Validation Report

Laporan validasi sementara berdasarkan 4 run yang sudah terkumpul.

**1. Completeness:** 40% data terkumpul (4/10 run)

**2. Format:** [x] Konsisten — semua file CSV dengan header dan tipe data yang sama

**3. Range check:**
- .NET: semua nilai p95 dalam range 3–7 ms — wajar untuk REST API lokal tanpa network overhead
- Spring Boot: p95 2.000–2.300 ms — tinggi, tapi konsisten antar-run (bukan outlier acak)
- Tidak ada nilai negatif, tidak ada nilai > 60.000 ms (timeout default k6)
- 3 POST 500 di dn-run-002 (0,07%) — dalam batas toleransi

**4. Logic check:** [x] Parameter sesuai plan
- VU=20, ramp=30s, steady=120s untuk semua run ✅
- Dataset identik (IKEA_product_catalog.csv, 401.046 dokumen) ✅
- Container resource limits identik (cpus=2, memory=2g) ✅
- Urutan eksekusi interleave terjaga: sb → dn → dn → sb ✅

**Kesimpulan:** [ ] Data siap analisis / [x] Perlu tindakan:
> Data 4 run yang ada sudah valid secara format dan range. Namun analisis statistik final belum bisa dilakukan — perlu menyelesaikan 6 run sisanya (sb-run-003 s/d sb-run-005, dn-run-003 s/d dn-run-005). Setelah semua 10 run terkumpul, lakukan validasi ulang dengan checklist lengkap sebelum melanjutkan ke WS-12.

---

## Refleksi

> Apa perbedaan antara "data yang benar" dan "data yang dipercaya"? Mengapa proses validasi formal diperlukan meskipun data dikumpulkan secara otomatis?

**Jawaban:**
> "Data yang benar" berarti nilai secara teknis akurat — misalnya logger mencatat 867 ms dan memang itu durasi request yang terjadi. "Data yang dipercaya" lebih luas: data harus benar, tetapi juga harus konsisten antar-run, lengkap sesuai rencana, dalam range yang masuk akal, dan dikumpulkan di bawah kondisi yang terkontrol.
>
> Logging otomatis seperti k6 `--out csv` bisa mencatat nilai yang benar secara teknis tetapi tidak bisa dipercaya untuk riset jika: container API belum warm saat pengukuran dimulai, ada background process yang mengganggu, atau konfigurasi parameter berubah antar-run tanpa tercatat. Proses validasi formal — cek format, range, konsistensi, dan logika — adalah cara untuk membuktikan bahwa kondisi pengukuran terpenuhi, bukan hanya bahwa angka tercatat. Tanpa validasi ini, klaim perbandingan kinerja tidak bisa dipertahankan di hadapan reviewer jurnal.
