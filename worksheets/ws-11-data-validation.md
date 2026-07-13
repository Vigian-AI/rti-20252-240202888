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
  [x] Semua skenario tercakup
  [x] Jumlah run sesuai rencana (5 per skenario)
  [x] Tidak ada file output hilang
  Missing: 0 dari 10 data points

Format Consistency:
  [x] Semua file format sama (CSV)
  [x] Header konsisten
  [x] Tipe data konsisten (numerik tetap numerik)

Range & Logic:
  [x] Nilai dalam range masuk akal (RPS > 0, latency > 0)
  [x] Tidak ada waktu negatif
  [x] Metrik 0–100% (error rate dalam range valid)
  Anomali ditemukan: sb-run-001 mengalami JIT cold-start (throughput lebih rendah, standard deviasi tinggi); error rate signifikan (~23-33%) di bawah beban tinggi akibat saturasi database MongoDB.

Cross-Validation:
  [x] Run identik → hasil mendekati (dn-run-001 s/d 005 sangat konsisten; sb-run-002 s/d 005 sangat konsisten)
  [x] Trend konsisten dengan ekspektasi teori (.NET memiliki throughput lebih tinggi dan latency lebih rendah dibanding Spring Boot)

Keputusan:
  [x] Data siap analisis
  [ ] Perlu cleaning
  [ ] Perlu re-run (skenario: —)
```

---

## Latihan 1 — Completeness Check

Status pengumpulan data per tanggal validasi ini (13 Juli 2026). Semua 10 run telah selesai dieksekusi.

| File | Skenario | Status | Jumlah Request | Catatan |
|------|----------|--------|----------------|---------|
| sb-run-001.csv | Spring Boot | ✅ Selesai | 2.535 | Valid, JIT cold-start terdeteksi |
| sb-run-002.csv | Spring Boot | ✅ Selesai | 3.216 | Valid |
| sb-run-003.csv | Spring Boot | ✅ Selesai | 3.441 | Valid |
| sb-run-004.csv | Spring Boot | ✅ Selesai | 3.355 | Valid |
| sb-run-005.csv | Spring Boot | ✅ Selesai | 3.160 | Valid |
| dn-run-001.csv | .NET | ✅ Selesai | 26.921 | Valid |
| dn-run-002.csv | .NET | ✅ Selesai | 27.068 | Valid |
| dn-run-003.csv | .NET | ✅ Selesai | 27.306 | Valid |
| dn-run-004.csv | .NET | ✅ Selesai | 27.153 | Valid |
| dn-run-005.csv | .NET | ✅ Selesai | 26.912 | Valid |

**Total expected:** 10 run | **Total actual:** 10 run | **Missing:** 0 run

**Keputusan untuk data missing:**
> Tidak ada data missing. Seluruh 10 run yang direncanakan telah berhasil dieksekusi secara lengkap (5 run untuk Spring Boot, 5 run untuk .NET) dengan urutan interleave untuk menghindari bias temporal/urutan. Data siap untuk analisis statistik dan interpretasi lanjut.

---

## Latihan 2 — Anomaly Investigation

Validasi 10 run yang sudah terkumpul menggunakan data aktual dari `riset-directory/06-output/`.

### Data saat ini (metrik p95 latency per run)

| Run | Skenario | n requests | RPS | Mean (ms) | Std Dev (ms) | p95 (ms) | p99 (ms) |
|-----|----------|-----------|-----|-----------|-------------|----------|----------|
| dn-run-001 | .NET | 26,921 | 224.34 | 3.40 | 2.20 | 5.37 | 7.24 |
| dn-run-002 | .NET | 27,068 | 225.57 | 2.81 | 1.96 | 4.93 | 6.39 |
| dn-run-003 | .NET | 27,306 | 227.55 | 1.93 | 1.89 | 2.98 | 4.05 |
| dn-run-004 | .NET | 27,153 | 226.28 | 2.54 | 1.98 | 4.51 | 6.20 |
| dn-run-005 | .NET | 26,912 | 224.27 | 3.45 | 2.57 | 5.41 | 7.09 |
| sb-run-001 | Spring Boot | 2,535 | 21.12 | 1008.39 | 1134.40 | 3297.05 | 4007.40 |
| sb-run-002 | Spring Boot | 3,216 | 26.80 | 773.16 | 824.12 | 2000.19 | 2298.15 |
| sb-run-003 | Spring Boot | 3,441 | 28.68 | 715.92 | 767.81 | 1806.27 | 2094.65 |
| sb-run-004 | Spring Boot | 3,355 | 27.96 | 736.99 | 770.86 | 1892.71 | 2100.15 |
| sb-run-005 | Spring Boot | 3,160 | 26.33 | 789.46 | 858.29 | 2097.07 | 2398.31 |

### Deteksi outlier antar-run (per skenario, metrik RPS)

**Spring Boot — RPS: [21.12, 26.80, 28.68, 27.96, 26.33]**
> Mean Spring Boot = 26.18, Std Dev = 2.98. Range normal IQR: Q1 = 26.33, Q3 = 27.96. IQR = 1.63. Lower Bound = Q1 - 1.5 * IQR = 23.88. Nilai `sb-run-001` (21.12 RPS) berada di bawah lower bound sehingga terdeteksi sebagai outlier statistis potensial. Hal ini terjadi karena JVM cold-start pada run pertama.

**.NET — RPS: [224.27, 224.34, 225.57, 226.28, 227.55]**
> Mean .NET = 225.60, Std Dev = 1.38. Selisih maksimum dan minimum sangat kecil (selisih 3.28 RPS atau ~1.4% dari mean), menunjukkan konsistensi yang luar biasa dan tidak ada outlier statistis.

**Anomali yang terdeteksi:**

| Anomali | Nilai | Kemungkinan Penyebab | Keputusan |
|---------|-------|---------------------|-----------|
| sb-run-001: Throughput rendah | 21.12 RPS (outlier statistis) | JVM JIT compilation overhead dan inisialisasi class pada run pertama (cold start) | Tetap disertakan, namun diberi catatan mengenai efek cold-start JVM |
| Spring Boot std dev sangat besar | Std dev = 1.134,4 ms pada sb-run-001 | Latensi sangat skewed akibat cold-start request yang lambat di awal (max > 4000ms) berbaur dengan request cepat | Dilaporkan, dan gunakan median/p95 sebagai metrik utama yang lebih robust dibanding mean |
| Error rate tinggi di kedua skenario | ~33% untuk .NET dan ~23% untuk Spring Boot | Saturasi resource database MongoDB di bawah beban 50 VUs CRUD berulang, memicu pool timeout | Analisis saturasi DB dilakukan di Tahap 4; data tetap valid untuk analisis batas kapasitas sistem |

### Konsistensi format

- [x] Semua 10 file berformat CSV
- [x] Header konsisten di semua file
- [x] Kolom `metric_value` bertipe float di semua file
- [x] Kolom `status` bertipe string integer (200, 201, 204, 404, 500)
- [x] Tidak ada nilai negatif pada `metric_value` untuk `http_req_duration`
- [x] Tidak ada baris dengan `metric_name = http_req_duration` yang memiliki `metric_value = 0`

---

## Latihan 3 — Validation Report

Laporan validasi final berdasarkan 10 run yang sudah terkumpul lengkap.

**1. Completeness:** 100% data terkumpul (10/10 run)

**2. Format:** [x] Konsisten — semua file CSV dengan header dan tipe data yang sama

**3. Range check:**
- .NET: semua nilai p95 dalam range 2.98 – 5.41 ms — konsisten cepat dan stabil.
- Spring Boot: semua nilai p95 dalam range 1806.27 – 3297.05 ms — tinggi, dengan variabilitas run pertama lebih tinggi karena JIT warm-up.
- Error rate berkisar ~33% (.NET) dan ~23% (Spring Boot) — tidak ada kegagalan run total (crash), semua run terselesaikan secara terstruktur.

**4. Logic check:** [x] Parameter sesuai plan
- VU=50, ramp=30s, steady=120s, warmup=30s untuk semua run.
- Dataset identik (IKEA_product_catalog.csv, 401.046 dokumen).
- Container resource limits identik (cpus=2, memory=2g).
- Urutan eksekusi interleave (SB -> DN -> DN -> SB -> SB -> DN -> DN -> SB -> SB -> DN) terlaksana.

**Kesimpulan:** [x] Data siap analisis / [ ] Perlu tindakan:
> Seluruh 10 run telah divalidasi dan memenuhi kriteria kualitas data (completeness, format consistency, range, dan logic). Meskipun terdapat anomali berupa performa rendah di run pertama Spring Boot (sb-run-001) akibat JIT warm-up dan error rate yang signifikan akibat DB saturation, hal ini mencerminkan karakteristik performa sistem yang sebenarnya di bawah batas kapasitas dan tidak merusak integritas eksperimen. Data siap untuk dianalisis di WS-12 dan WS-14.

---

## Refleksi

> Apa perbedaan antara "data yang benar" dan "data yang dipercaya"? Mengapa proses validasi formal diperlukan meskipun data dikumpulkan secara otomatis?

**Jawaban:**
> "Data yang benar" berarti nilai secara teknis akurat — misalnya logger mencatat 867 ms dan memang itu durasi request yang terjadi. "Data yang dipercaya" lebih luas: data harus benar, tetapi juga harus konsisten antar-run, lengkap sesuai rencana, dalam range yang masuk akal, dan dikumpulkan di bawah kondisi yang terkontrol.
>
> Logging otomatis seperti k6 `--out csv` bisa mencatat nilai yang benar secara teknis tetapi tidak bisa dipercaya untuk riset jika: container API belum warm saat pengukuran dimulai, ada background process yang mengganggu, atau konfigurasi parameter berubah antar-run tanpa tercatat. Proses validasi formal — cek format, range, konsistensi, dan logika — adalah cara untuk membuktikan bahwa kondisi pengukuran terpenuhi, bukan hanya bahwa angka tercatat. Tanpa validasi ini, klaim perbandingan kinerja tidak bisa dipertahankan di hadapan reviewer jurnal.
