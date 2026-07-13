# WS-12: Result Presentation & Visualization

> **Bab 12 — Penyajian Hasil & Visualisasi**

---

## Ringkasan Materi

### Data → Insight Model

```
Validated Data → Structured Presentation → Visualization → Pattern Recognition → Insight
```

Penyajian **mendahului** analisis. Tabel dan grafik membantu peneliti "melihat" data sebelum menghitung. Langsung ke uji statistik tanpa visualisasi berisiko kesimpulan yang secara teknis benar tapi kontekstual salah (Anscombe's Quartet, 1973).

### Tabel = Presisi, Grafik = Pola

Keduanya **saling melengkapi**:
- Tabel: angka presisi, self-contained (dipahami tanpa teks), sortable
- Grafik: pola visual, tren, perbandingan cepat

### Jenis Grafik Berdasarkan Tujuan

| Tujuan | Jenis Grafik |
|--------|-------------|
| Perbandingan antar-skenario | Bar chart (grouped/stacked) |
| Distribusi per-skenario | Box plot / violin plot |
| Tren temporal | Line chart |
| Korelasi dua variabel | Scatter plot |
| Proporsi (total = 100%) | Pie chart (hati-hati!) |

### Contoh Tabel Hasil yang Baik

| Model | Accuracy (%) | F1-Score (%) | Training Time (min) |
|-------|-------------|-------------|---------------------|
| BERT | 88.4 ± 1.2 | 87.1 ± 1.4 | 45.2 ± 3.1 |
| LSTM | 86.1 ± 1.8 | 84.5 ± 2.0 | 12.8 ± 1.2 |
| SVM | 82.3 ± 0.9 | 80.7 ± 1.1 | 0.3 ± 0.1 |

*N=10 per model. Mean ± std. Diurutkan berdasarkan Accuracy.*

### Visualization Bias — Yang Harus Dihindari

| Bias | Deskripsi | Dampak |
|------|----------|--------|
| Truncated axis | Y tidak dari 0 | Memperbesar perbedaan kecil |
| Inconsistent scale | Dua grafik skala beda | Perbandingan menyesatkan |
| Cherry-picked data | Hanya tampilkan yang "menang" | Selektif, tidak jujur |
| 3D effects | Efek 3D tanpa dimensi data ke-3 | Distorsi tanpa informasi |
| Missing error bar | Tidak ada variabilitas | Menyembunyikan ketidakpastian |

### Engineering vs Research Presentation

| Aspek | Engineering | Research |
|-------|-----------|---------|
| Tujuan grafik | Dashboard monitoring | Mendukung argumen ilmiah |
| Informasi wajib | KPI, threshold | Mean, std, CI, N, p-value |
| Bias handling | Less critical | Wajib dihindari (peer-review) |

---

## Template A.12 — Result Presentation Plan

```
RESULT PRESENTATION PLAN

Research Question : Apakah terdapat perbedaan signifikan dalam throughput (RPS) dan p95 latency (ms) antara aplikasi REST API yang dibangun menggunakan Java Spring Boot dan .NET saat melakukan operasi CRUD pada database MongoDB?
Metrik Utama      : Throughput (RPS) dan p95 Latency (ms)

Tabel Hasil:
| Skenario | Throughput (RPS) (mean ± std) | p95 Latency (ms) (mean ± std) | n |
|----------|-------------------------------|------------------------------|---|
| .NET     | 225.60 ± 1.38                 | 4.64 ± 1.00                  | 5 |
| Spring Boot | 26.18 ± 2.98                 | 2218.66 ± 612.73            | 5 |

Visualisasi yang Direncanakan:
| # | Jenis Grafik | Pesan Utama | Metrik |
|---|-------------|-------------|--------|
| 1 | Bar Chart + Error Bar | Perbandingan throughput (RPS) antara Spring Boot dan .NET | Mean Throughput (RPS) ± std |
| 2 | Box Plot | Distribusi p95 Latency per run untuk melihat konsistensi dan penyebaran | p95 Latency (ms) per run |
| 3 | Bar Chart + Error Bar | Perbandingan p95 Latency (ms) antara Spring Boot dan .NET | Mean p95 Latency (ms) ± std |

Bias Check:
  [x] Y-axis mulai dari 0 (atau dijustifikasi)
  [x] Error bar/CI ditampilkan
  [x] Semua data disertakan (tidak cherry-picked)
  [x] Tidak menggunakan 3D tanpa alasan
```

---

## Latihan 1 — Tabel Hasil

Buat tabel hasil eksperimen Anda (boleh dengan data simulasi jika belum punya data riil).

| Skenario | Throughput (RPS) (mean ± std) | p95 Latency (ms) (mean ± std) | n |
|----------|-------------------------------|------------------------------|---|
| .NET     | 225.60 ± 1.38                 | 4.64 ± 1.00                  | 5 |
| Spring Boot | 26.18 ± 2.98                 | 2218.66 ± 612.73            | 5 |

**Checklist tabel:**
- [x] Self-contained (judul jelas, satuan ada, N tercantum)
- [x] Mean ± std (bukan single number)
- [x] Diurutkan berdasarkan metrik utama (Throughput)
- [x] Format konsisten di semua baris

---

## Latihan 2 — Rencana Visualisasi

Rencanakan 2-3 grafik untuk menyajikan data dari Latihan 1. Setiap grafik = satu pesan.

| # | Jenis Grafik | Pesan | Data yang Digunakan |
|---|-------------|-------|---------------------|
| 1 | Bar chart + error bar | .NET memiliki throughput (RPS) jauh lebih tinggi (>8.6x) secara konsisten dibanding Spring Boot | Mean throughput (RPS) ± std |
| 2 | Box plot | Distribusi p95 latency .NET sangat sempit dan rendah, sedangkan Spring Boot sangat bervariasi dengan rentang lebar | Semua 5 run p95 latency (ms) per skenario |
| 3 | Bar chart + error bar | .NET memiliki p95 latency jauh lebih rendah (fast response) secara signifikan dibanding Spring Boot | Mean p95 latency (ms) ± std |

---

## Latihan 3 — Bias Detection

Evaluasi visualisasi berikut untuk bias (skenario dari contoh):

**Skenario:** Metode A = 91.2%, Metode B = 90.8%. Bar chart dengan Y-axis mulai dari 90%.

| Pertanyaan | Jawaban |
|-----------|---------|
| Apakah Y-axis menyesatkan? | Ya — Y-axis yang dimulai dari 90% membuat perbedaan visual terlihat sangat besar (Metode A terlihat 1.5x hingga 2x lebih tinggi dari Metode B), padahal perbedaan sebenarnya hanya 0.4% secara absolut. |
| Apakah error bar ditampilkan? | Tidak — tanpa error bar kita tidak bisa mengetahui apakah perbedaan 0.4% tersebut merupakan perbedaan nyata yang signifikan atau hanya noise variansi eksperimen. |
| Apakah semua kondisi ditampilkan? | Tidak disebutkan, namun membatasi sumbu Y dan tidak menampilkan variabilitas berpotensi menyembunyikan kelemahan/stabilitas data (cherry-picking visual). |
| Apa solusinya? | Memulai Y-axis dari 0% agar representasi visual proporsional dengan nilainya, dan menambahkan error bar (standar deviasi/selang kepercayaan) pada setiap bar. |

**Evaluasi grafik Anda sendiri dari Latihan 2:**
- [x] Semua bias check lulus
- [x] Ada yang perlu diperbaiki: Tidak ada, semua grafik dirancang dengan Y-axis mulai dari 0, menampilkan error bar standar deviasi, dan menggunakan seluruh data run yang terkumpul secara transparan.

---

## Refleksi

> Mengapa tabel dan grafik keduanya diperlukan — tidak cukup salah satu saja? Pernahkah Anda membuat grafik yang (tanpa sengaja) menyesatkan?

Tabel dan grafik saling melengkapi dalam penyajian hasil riset karena menyasar kebutuhan kognitif yang berbeda. Tabel memberikan presisi numerik yang tinggi, bersifat mandiri (self-contained), dan memungkinkan pembaca melihat nilai eksak beserta variabilitas statistik (seperti standar deviasi atau confidence interval) secara detail. Sementara itu, grafik memberikan pola visual yang instan, mempermudah identifikasi tren makro, visualisasi perbandingan antar-skenario secara langsung, serta visualisasi bentuk distribusi data (seperti penyebaran box plot) yang sulit ditangkap dengan cepat hanya dari deretan angka tabel.

Saya pernah secara tidak sengaja membuat grafik yang menyesatkan saat belajar visualisasi di perkuliahan awal, di mana Y-axis pada grafik garis (line chart) di-autoscale oleh library pemrograman sehingga tidak mulai dari nol. Hal ini membesar-besarkan fluktuasi kecil kinerja yang sebenarnya hanya noise (kurang dari 1%) menjadi tampak seperti penurunan performa yang kritis bagi sistem. Sejak saat itu, saya menyadari bahwa penentuan rentang sumbu sumbu Y secara jujur dan penyajian variabilitas data melalui error bar adalah keharusan ilmiah.
