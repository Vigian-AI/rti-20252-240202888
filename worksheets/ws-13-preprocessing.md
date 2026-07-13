# WS-13: Data Preprocessing

> **Bab 13 — Preprocessing & Persiapan Data untuk Analisis**

---

## Ringkasan Materi

### Data Refinement Pipeline

```
Raw Data → Cleaning → Transformation → Normalization → Processed Data → Analysis Ready
```

Setiap tahap memiliki tujuan berbeda. **Preprocessing bukan langkah teknis biasa** — setiap keputusan preprocessing adalah keputusan riset yang bisa mengubah kesimpulan.

### Empat Prinsip Preprocessing

| Prinsip | Deskripsi |
|---------|----------|
| **Consistency** | Metode sama untuk data yang sama |
| **Transparency** | Setiap langkah terdokumentasi |
| **Reproducibility** | Orang lain bisa mengulang dengan hasil sama |
| **Minimal Distortion** | Ubah sesedikit mungkin; jika normalisasi tidak perlu, jangan lakukan |

### Cleaning Triad

| Masalah | Strategi | Risiko |
|---------|---------|--------|
| **Missing values** | | |
| — Listwise deletion | Missing < 5%, random | Data loss |
| — Mean/median imputation | Sedikit missing, dist. normal | Mengurangi variabilitas |
| — Model-based imputation | Banyak missing, pola sistematis | Introduces dependency |
| — Flag & separate | Missing karena alasan substantif | Kompleksitas analisis |
| **Duplikat** | Identifikasi → verifikasi → hapus | False positive (data mirip ≠ duplikat) |
| **Error format** | Standardisasi tipe, encoding | Kehilangan informasi saat konversi |

### Normalisasi — Kapan & Metode Mana

| Metode | Formula | Output | Sensitif Outlier? |
|--------|---------|--------|-------------------|
| Min-max | (x-min)/(max-min) | [0, 1] | Ya |
| Z-score | (x-mean)/std | Unbounded | Lebih robust |
| Robust scaling | (x-median)/IQR | Unbounded | Paling robust |

**Kunci:** Parameter normalisasi harus dihitung dari **training set saja** — bukan seluruh data. Pelanggaran = **data leakage**.

### Data Leakage Prevention

Data leakage terjadi ketika informasi dari test set "bocor" ke preprocessing:
- Normalisasi parameter dari seluruh dataset ← **SALAH**
- Cross-validation dilakukan sebelum split ← **SALAH**
- Feature selection menggunakan label test set ← **SALAH**

### Jebakan Kognitif

1. "Preprocessing cuma teknis — tidak perlu detail" → bisa ubah kesimpulan
2. "Lebih banyak preprocessing = lebih bersih = lebih baik" → over-processing distorsi data
3. "Normalisasi selalu diperlukan" → belum tentu, tergantung metode analisis
4. "Imputation sama untuk semua situasi" → strategi harus sesuai konteks

---

## Template A.13 — Preprocessing Documentation Log

```
PREPROCESSING LOG

Dataset           : IKEA Product Catalog (IKEA_product_catalog.csv) & k6 Benchmark Logs
Jumlah data awal  : 401.046 dokumen (Catalog) & 10 runs (k6 Logs)

Cleaning:
| Masalah | Jumlah Kasus | Penanganan | Justifikasi |
|---------|-------------|------------|-------------|
| Missing | Variabel rating/price kosong | Diubah menjadi null (None) | Data missing bersifat MCAR, null mencegah error query |
| Duplikat| 0 kasus | unique_id di-index unik | Data input sudah bersih dari duplikat id |
| Error   | Format string untuk angka | Parsing string -> float | Nilai numerik harus dalam tipe float untuk aggregasi |

Transformation:
| Transformasi | Variabel | Detail | Alasan |
|-------------|----------|--------|--------|
| Exclude Warmup | http_req_duration | Menghapus data dari 30s pertama | Menghindari skewness akibat pemanasan JVM/JIT compiler |
| Aggregation | k6 log per request | Hitung mean, p95, p99, RPS, error_rate | Menyederhanakan jutaan baris request log menjadi 10 run |

Normalization:
  Metode    : Tidak memerlukan normalisasi
  Alasan    : Metrik utama (RPS dan ms) adalah skala rasio yang bermakna fisik langsung dan uji statistik komparatif tidak memerlukannya.
  Parameter : N/A

Leakage Check:
  [x] Parameter normalisasi dari training set saja (N/A)
  [x] Tidak ada informasi test set dalam preprocessing (N/A)
  [x] Cross-validation dilakukan setelah split (N/A)

Jumlah data akhir : 401.046 dokumen (Catalog) & 10 records di all_runs.csv (k6 Logs)
Script tersedia   : [x] Ya → path: riset-directory/05-kode/scripts/import_data.py & extract_metrics.py | [ ] Belum
```

---

## Latihan 1 — Cleaning Plan

Periksa dataset Anda (atau dataset contoh) dan dokumentasikan masalah yang ditemukan.

| Masalah | Jumlah Kasus | Penanganan | Justifikasi |
|---------|-------------|------------|-------------|
| Missing value di kolom `product_rating`, `product_rating_count`, `price` | ~6.500 kasus rating kosong/none | Konversi string "none" atau kosong ke `None` (Null) | Mencegah error tipe data saat di-import ke MongoDB dan kalkulasi |
| Error format numerik pada kolom `price`, `product_rating` | Semua kolom bertipe string di CSV | Parsing string ke float menggunakan `float()` di python | Memungkinkan komputasi query agregasi database secara native |
| Duplikasi ID kandidat pada `unique_id` | 0 kasus (terdeteksi saat import) | Skrip import_data.py menggunakan ordered=False dan unique index | Menjamin integritas constraint unique_id di database |

**Jumlah data sebelum cleaning:** 401.046 dokumen
**Jumlah data setelah cleaning:** 401.046 dokumen
**Persentase data yang hilang/berubah:** 0.00% (tidak ada dokumen yang dibuang, hanya format nilainya yang dibersihkan/dikonversi)

---

## Latihan 2 — Normalisasi Decision

Tentukan apakah data Anda perlu normalisasi, dan jika ya, metode apa yang tepat.

| Variabel | Range Asli | Distribusi | Outlier? | Metode Normalisasi | Alasan |
|----------|-----------|-----------|----------|-------------------|--------|
| `throughput_rps` | 21.12 – 227.55 | Normal per skenario | Tidak | Tidak perlu | Metrik performa dengan arti fisik yang jelas, siap untuk t-test |
| `p95_latency_ms` | 2.98 – 3297.05 | Skewed (Spring Boot tinggi, .NET rendah) | Tidak | Tidak perlu | Metrik latency bermakna fisik. Uji Mann-Whitney U menggunakan rank sehingga invariant terhadap normalisasi |

**Apakah normalisasi diperlukan?** [ ] Ya / [x] Tidak
**Justifikasi:**
> Metrik throughput (RPS) dan latency (ms) memiliki interpretabilitas fisik yang sangat penting untuk penulisan ilmiah. Melakukan normalisasi (misal min-max atau z-score) akan menghilangkan satuan fisik aslinya dan tidak memberikan keuntungan apa pun, karena uji statistik induktif yang kami jalankan (Independent t-test dan Mann-Whitney U) dapat memproses data mentah tersebut secara langsung.

**Leakage check:**
- [x] Parameter dihitung dari training set saja (N/A)
- [x] Normalisasi diterapkan setelah train-test split (N/A)

---

## Latihan 3 — Preprocessing Report

Buat ringkasan preprocessing lengkap — dokumentasi yang cukup bagi orang lain untuk mereplikasi.

```
PREPROCESSING SUMMARY

1. Dataset: IKEA Product Catalog (IKEA_product_catalog.csv) & k6 Benchmark Logs
2. Data awal: 401.046 records, 18 features (Catalog) | 10 CSV run log k6
3. Cleaning:
   - Missing values: Mengubah string "none"/kosong pada rating/count/price ke Null, metode: conditional parsing
   - Duplikat: 0 kasus, tindakan: validasi via MongoDB unique index pada unique_id
   - Error: Format data string numerik, tindakan: parsing ke float tipe data
4. Transformation: Memfilter dan membuang data request pada 30 detik pertama (warmup phase) dari k6 logs, menyisakan 120 detik steady-state
5. Normalisasi: Tidak diperlukan (metode), parameter dari N/A
6. Data akhir: 401.046 dokumen di MongoDB | 10 baris agregat di results/all_runs.csv
7. Leakage check: [x] Lulus / [ ] Ada masalah
```

---

## Refleksi

> Apakah Anda pernah melakukan normalisasi "karena biasa dilakukan" tanpa mempertimbangkan apakah benar-benar diperlukan? Apa risiko over-preprocessing?

Ya, dalam beberapa eksperimen machine learning terdahulu, sering kali ada kecenderungan untuk langsung menerapkan Min-Max Scaler atau Standard Scaler pada seluruh fitur numerik secara refleks tanpa menganalisis apakah model yang digunakan memerlukannya. Sebagai contoh, algoritma berbasis pohon keputusan seperti Random Forest atau XGBoost bersifat invariant terhadap skala fitur, sehingga preprocessing normalisasi sebenarnya tidak diperlukan dan hanya membuang resource komputasi.

Risiko dari over-preprocessing meliputi:
1. **Kehilangan Makna Fisik (Interpretability):** Nilai latency dalam milidetik atau throughput dalam RPS jauh lebih mudah dipahami oleh pembaca daripada nilai z-score yang bernilai negatif atau nilai min-max di rentang [0, 1].
2. **Distorsi Distribusi Data:** Terutama jika menggunakan Min-Max scaling pada dataset yang memiliki outlier ekstrem, rentang data normal akan terkompresi ke area yang sangat sempit, mengurangi resolusi informasi.
3. **Data Leakage:** Jika parameter normalisasi (seperti mean, standard deviation, min, atau max) dihitung dari seluruh dataset sebelum proses split (train-test split atau cross-validation), informasi dari data uji akan bocor ke model pelatihan, menghasilkan estimasi performa yang overoptimistic dan tidak valid secara ilmiah.
