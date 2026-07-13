# Laporan Penelitian

**Judul:** Analisis Komparatif Performa REST API Java Spring Boot vs .NET Core pada Operasi CRUD Database MongoDB

**Peneliti:** Vigian Agus Isnaeni 240202888
**Target Publikasi:** TIIJ
**Status Penelitian:** selesai [../07-manuskrip/TIIJ.md](../07-manuskrip/TIIJ.md)

---

## 1. Ringkasan Eksekutif

Penelitian ini membandingkan kinerja Java Spring Boot vs .NET Core dalam penanganan REST API yang terhubung dengan database NoSQL MongoDB di bawah batasan resource container (2 vCPU, 2GB RAM). Pengujian dilakukan melalui eksperimen beban terkontrol (load testing) menggunakan k6 dengan parameter 50 Virtual Users (VUs) konstan selama 120 detik steady-state didahului 30 detik warm-up. Eksperimen mencakup 10 run secara interleave (5 run per framework) untuk menguji metrik throughput (RPS), p95 latency (ms), dan error rate (%) secara empiris.

**Temuan utama:**
* **Throughput:** .NET Core menghasilkan throughput rata-rata sebesar 225.60 ± 1.38 RPS, yang ~8.6x lebih tinggi secara signifikan (p < 0.05, Cohen's d = -85.97) dibanding Spring Boot (26.18 ± 2.98 RPS).
* **Latency (p95):** .NET Core memiliki respon p95 rata-rata sebesar 4.64 ± 1.00 ms, yang ~478x lebih cepat secara signifikan (p < 0.05, Cohen's d = 5.11) dibanding Spring Boot (2218.66 ± 612.73 ms).
* **JIT & Warmup:** Spring Boot mengalami fluktuasi latensi ekstrim pada run pertama (3297.05 ms) karena kompilasi JIT (cold start) dan alokasi memory JVM, lalu mendatar di kisaran 1800–2100 ms pada run-run berikutnya.
* **Trade-off Database Saturation:** Laju pemrosesan request .NET Core yang sangat tinggi memicu kejenuhan pool koneksi database MongoDB lokal, menghasilkan error rate yang lebih tinggi (~33.27% vs ~23.38% pada Spring Boot). Lambatnya respon Spring Boot bertindak sebagai backpressure alami yang membatasi beban masuk ke database.

---

## 2. Latar Belakang dan Rumusan Masalah

### 2.1 Latar Belakang
Pemilihan framework backend untuk arsitektur microservices modern sering kali didominasi oleh preferensi subjektif developer atau tren pasar daripada pembuktian empiris. Masalah ini menjadi kritis ketika aplikasi dijalankan pada lingkungan containerized (seperti Docker atau Kubernetes) yang dibatasi resource CPU dan memorinya untuk meminimalkan biaya infrastruktur cloud. Java Spring Boot (JVM) dan .NET Core (CLR) adalah dua framework enterprise utama yang bersaing di segmen ini. Namun, evaluasi empiris mengenai bagaimana keduanya menangani konkurensi dan database I/O bound pada database NoSQL seperti MongoDB dengan pembatasan resource masih sangat terbatas.

### 2.2 Rumusan Masalah
1. Apakah terdapat perbedaan performa throughput (RPS) yang signifikan secara statistik antara REST API Java Spring Boot dan .NET Core saat melakukan operasi CRUD pada database MongoDB di bawah batasan resource container?
2. Apakah terdapat perbedaan p95 latency (ms) yang signifikan secara statistik antara kedua framework tersebut?
3. Bagaimana dampak JIT compilation (warm-up) JVM dan pembatasan CPU container terhadap stabilitas latensi Spring Boot?
4. Bagaimana trade-off antara kecepatan pemrosesan request dengan keandalan (error rate) koneksi database MongoDB pada kedua framework di bawah beban tinggi?

### 2.3 Tujuan Penelitian
Tujuan dari penelitian ini adalah menyajikan analisis komparatif performa kuantitatif yang objektif dan dapat direproduksi untuk memandu para arsitek perangkat lunak dalam memilih framework backend optimal di bawah batasan resource infrastruktur container Docker.

---

## 3. Metodologi dan Pelaksanaan

Penelitian dilaksanakan dalam 5 tahap:

### 3.1 Tahap 1 — Perancangan Arsitektur & Skema Database
**Status: Selesai.** Dirancang arsitektur benchmark di mana REST API (Spring Boot atau .NET) berjalan pada container terpisah dan terhubung ke instance database MongoDB 7.0 lokal. Dataset yang digunakan adalah katalog produk IKEA sebanyak 401.046 dokumen yang di-import sekali sebelum pengujian dimulai. Skema database MongoDB dirancang dengan index unik pada `unique_id` untuk memastikan optimasi pencarian data CRUD.
Detail & diagram: [../03-teori/arsitektur-dan-skema.md](../03-teori/arsitektur-dan-skema.md).

### 3.2 Tahap 2 — Implementasi REST API
**Status: Selesai.** Diimplementasikan dua aplikasi API Gateway CRUD yang secara fungsional identik:
* **Spring Boot API:** Menggunakan Java 21, Spring Boot 3.x, Spring Data MongoDB.
* **.NET API:** Menggunakan .NET 8 Web API, MongoDB.Driver NuGet package.
Kedua aplikasi dideploy menggunakan Docker Compose dengan CPU limit dikunci pada `cpus: 2` dan memory limit pada `memory: 2g` untuk mensimulasikan resource container kecil.

### 3.3 Tahap 3 — Pengujian Beban k6
**Status: Selesai.** Load testing menggunakan k6 dijalankan secara terstruktur sebanyak 10 run (5 run per framework) secara interleave (SB-DN-DN-SB-SB-DN-DN-SB-SB-DN) untuk menghilangkan bias thermal. Parameter k6 dikunci pada 50 Virtual Users (VUs) selama 150 detik total (30s warm-up dan 120s steady-state). Data warm-up diabaikan untuk menjamin keadilan pengukuran.
Hasil data mentah k6 diekstrak dari CSV per request menjadi dataset agregat `results/all_runs.csv`.

### 3.4 Tahap 4 — Ekstraksi Data & Analisis Statistik
**Status: Selesai.** Menggunakan pipeline analisis Python dengan library `scipy.stats` dan `pandas` untuk:
* Melakukan uji normalitas Shapiro-Wilk untuk memvalidasi sebaran data.
* Menjalankan uji parametrik Independent t-test untuk throughput dan uji non-parametrik Mann-Whitney U untuk p95 latency.
* Menghitung effect size Cohen's d.
* Menghasilkan visualisasi diagram batang (Mean ± SD) untuk throughput dan latency.

---

## 4. Hasil Penelitian

### 4.1 Statistik Deskriptif Hasil Pengujian

| Run | Skenario | n requests | RPS | Mean (ms) | Std Dev (ms) | p95 (ms) | p99 (ms) | Error Rate (%) |
|-----|----------|-----------|-----|-----------|-------------|----------|----------|----------------|
| dn-run-001 | dotnet | 26,921 | 224.34 | 3.40 | 2.20 | 5.37 | 7.24 | 32.80% |
| dn-run-002 | dotnet | 27,068 | 225.57 | 2.81 | 1.96 | 4.93 | 6.39 | 33.21% |
| dn-run-003 | dotnet | 27,306 | 227.55 | 1.93 | 1.89 | 2.98 | 4.05 | 33.65% |
| dn-run-004 | dotnet | 27,153 | 226.28 | 2.54 | 1.98 | 4.51 | 6.20 | 33.91% |
| dn-run-005 | dotnet | 26,912 | 224.27 | 3.45 | 2.57 | 5.41 | 7.09 | 33.06% |
| sb-run-001 | spring-boot | 2,535 | 21.12 | 1008.39 | 1134.40 | 3297.05 | 4007.40 | 22.88% |
| sb-run-002 | spring-boot | 3,216 | 26.80 | 773.16 | 824.12 | 2000.19 | 2298.15 | 22.95% |
| sb-run-003 | spring-boot | 3,441 | 28.68 | 715.92 | 767.81 | 1806.27 | 2094.65 | 23.86% |
| sb-run-004 | spring-boot | 3,355 | 27.96 | 736.99 | 770.86 | 1892.71 | 2100.15 | 23.25% |
| sb-run-005 | spring-boot | 3,160 | 26.33 | 789.46 | 858.29 | 2097.07 | 2398.31 | 23.96% |

### 4.2 Uji Hipotesis & Effect Size

* **Throughput (RPS):**
  * Shapiro-Wilk: Spring Boot p = 0.1357 (Normal), .NET Core p = 0.5306 (Normal).
  * Uji Signifikansi: Independent t-test menghasilkan p = 0.0000 (Signifikan pada alpha = 0.05).
  * Effect Size: Cohen's d = -85.97 (sangat besar).
  * 95% Confidence Interval: [-203.07, -195.78] RPS.
* **p95 Latency (ms):**
  * Shapiro-Wilk: Spring Boot p = 0.0155 (Tidak Normal), .NET Core p = 0.1495 (Normal).
  * Uji Signifikansi: Mann-Whitney U menghasilkan p = 0.0079 (Signifikan pada alpha = 0.05).
  * Effect Size: Cohen's d = 5.11 (sangat besar).
  * 95% Confidence Interval: [1453.22, 2974.82] ms.

### 4.3 Visualisasi

* **Throughput Comparison:** [../06-output/throughput_comparison.png](../06-output/throughput_comparison.png)
* **p95 Latency Comparison:** [../06-output/latency_comparison.png](../06-output/latency_comparison.png)

---

## 5. Kendala dan Catatan Lingkungan

* **JVM Warm-up & CPU Throttling:** Pada run pertama Spring Boot (`sb-run-001`), latency sangat bervariasi dengan standar deviasi 1134.40 ms dan p95 mencapai 3297.05 ms. Hal ini dipicu oleh JIT compiler overhead dan aktivitas garbage collection (Stop-The-World) yang intens dalam batasan 2 vCPU container.
* **Saturasi Database:** .NET Core memproses request sangat cepat (~225 RPS), yang menyebabkan overload koneksi ke database MongoDB lokal. Ini berakibat pada error rate yang lebih tinggi (~33.27%). Spring Boot yang lambat (~26 RPS) secara alami menerapkan backpressure sehingga database tidak mengalami saturasi ekstrim, menjaga error rate lebih rendah (~23.38%).
* **File CSV Sangat Besar:** Output raw k6 CSV berukuran ~52MB per run. File-file ini dihapus dari pelacakan Git (untracked) dan ditambahkan ke `.gitignore` untuk menjaga kapasitas repositori tetap ringan.

---

## 6. Kesimpulan dan Saran

* **Kesimpulan:** .NET Core terbukti memiliki performa throughput yang lebih tinggi (~8.6x) dan latency p95 yang jauh lebih cepat (~478x) secara signifikan dibanding Java Spring Boot pada CRUD MongoDB dalam resource container terbatas. Namun, terdapat trade-off di mana throughput ekstrim .NET Core memicu database saturation yang meningkatkan error rate.
* **Saran:**
  1. Penelitian berikutnya disarankan menguji Spring Native (AOT compilation) untuk meminimalkan cold-start dan penggunaan resource JVM.
  2. Implementasi connection pool tuning pada MongoDB driver diperlukan untuk mengatasi saturasi database di bawah framework berkinerja tinggi seperti .NET.

---

## 7. Lampiran — Peta Artefak Penelitian

| Direktori | Deskripsi | Status |
|---|---|---|
| [worksheets/](../worksheets/) | Worksheet tugas kuliah (WS-11 s/d WS-15) | Selesai |
| [riset-directory/03-teori/](../riset-directory/03-teori/) | Desain arsitektur dan skema database (Mermaid) | Selesai |
| [riset-directory/05-kode/scripts/](../riset-directory/05-kode/scripts/) | Script benchmark, ekstraksi metrik, dan analisis statistik | Selesai |
| [riset-directory/06-output/](../riset-directory/06-output/) | Agregat data (`all_runs.csv`), ringkasan statistik, dan visualisasi chart | Selesai |
| [riset-directory/07-manuskrip/](../riset-directory/07-manuskrip/) | Draf paper ilmiah lengkap (format TIIJ) | Selesai |
| [riset-directory/08-laporan/](../riset-directory/08-laporan/) | Laporan akhir penelitian (dokumen ini) | Selesai |
