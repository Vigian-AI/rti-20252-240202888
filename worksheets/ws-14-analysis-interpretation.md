# WS-14: Analysis, Interpretation & Failure Analysis

> **Bab 14 — Analisis Data, Interpretasi & Failure Analysis**

---

## Ringkasan Materi

### Data → Knowledge Model

```
Data → Analysis → Interpretation → Explanation → Knowledge
```

Tiga level yang berbeda:
- **Analysis** — "Apa yang terjadi?" (deskriptif + inferensial)
- **Interpretation** — "Apa artinya?" (konteks RQ + literatur)
- **Failure Analysis** — "Mengapa tidak berhasil?" (boundary conditions)

### Beyond p-value

**Statistical significance ≠ practical significance.** Selalu laporkan:
1. p-value (signifikansi statistik)
2. Effect size (besarnya efek)
3. Confidence interval (rentang ketidakpastian)

| Effect Size (Cohen's d) | Interpretasi |
|-------------------------|-------------|
| < 0.2 | Small |
| 0.2 – 0.8 | Medium |
| > 0.8 | Large |

### Pemilihan Uji Statistik

| Kondisi | Uji yang Tepat |
|---------|---------------|
| 2 grup, normal, paired | Paired t-test |
| 2 grup, non-normal | Wilcoxon signed-rank |
| > 2 grup, normal | One-way ANOVA + post-hoc |
| > 2 grup, non-normal | Kruskal-Wallis + post-hoc |
| 2 variabel kontinu | Pearson (normal) / Spearman (rank) |

### Failure Analysis as Contribution

Hipotesis yang ditolak adalah **temuan yang berharga**:

| Dataset | New (F1) | Baseline (F1) | p-value | Cohen's d |
|---------|---------|--------------|---------|-----------|
| DS-1 (small, clean) | 94.2±1.1 | 89.3±1.5 | <0.001 | **3.7** |
| DS-4 (medium, noisy) | 78.3±3.2 | 82.1±2.8 | 0.008 | **-1.3** |
| DS-5 (large, noisy) | 71.6±4.1 | 80.5±3.0 | <0.001 | **-2.5** |

**Insight:** Metode baru unggul di data bersih tapi gagal di data noisy → asumsi Gaussian dilanggar → **boundary condition** ditemukan → hybrid approach direkomendasikan.

**Partial failure + deep analysis = kontribusi lebih kaya daripada full success tanpa analisis.**

### Limitation Types

| Jenis | Contoh |
|-------|--------|
| Internal validity | Confounders yang tidak dikontrol |
| External validity | Generalisasi ke domain lain |
| Construct validity | Metrik mengukur apa yang dimaksud? |
| Statistical limitation | Sample size, asumsi distribusi |

### Jebakan Kognitif

1. "Signifikan statistik = penting secara praktis" → cek effect size
2. "Hipotesis tidak didukung → cari sudut baru" → p-hacking
3. "Kegagalan tidak perlu dilaporkan detail" → missed insight
4. "Limitasi cukup disebutkan, tidak perlu dianalisis" → kedalaman hilang

---

## Template A.14 — Analysis & Interpretation Report

```
ANALYSIS & INTERPRETATION

1. Statistik Deskriptif:
   | Skenario | Mean | Std | Median | Min | Max | n |
   |----------|------|-----|--------|-----|-----|---|
   | .NET Throughput (RPS) | 225.60 | 1.38 | 225.57 | 224.27 | 227.55 | 5 |
   | Spring Boot Throughput (RPS) | 26.18 | 2.98 | 26.80 | 21.12 | 28.68 | 5 |
   | .NET p95 Latency (ms) | 4.64 | 1.00 | 4.93 | 2.98 | 5.41 | 5 |
   | Spring Boot p95 Latency (ms) | 2218.66 | 612.73 | 2000.19 | 1806.27 | 3297.05 | 5 |

2. Uji Hipotesis:
   Uji yang digunakan  : Independent t-test (Throughput) & Mann-Whitney U (p95 Latency)
   Justifikasi          : Throughput Spring Boot (p=0.1357) dan .NET (p=0.5306) terdistribusi normal (Shapiro-Wilk, p > 0.05). Latency Spring Boot tidak normal (p=0.0155 <= 0.05), sehingga menggunakan Mann-Whitney U.
   Hasil: Throughput: p = 0.0000, effect size (d) = -85.97 | Latency: p = 0.0079, effect size (d) = 5.11
   CI 95%               : Throughput: [-203.07, -195.78] RPS | Latency: [1453.22, 2974.82] ms (Perbedaan SB - DN)

3. Keputusan:
   [x] H₀ ditolak → H₁ diterima
   [ ] H₀ tidak ditolak

4. Interpretasi:
   Hubungan ke RQ       : Terdapat perbedaan yang sangat signifikan dalam throughput (RPS) dan p95 latency (ms) antara Spring Boot dan .NET pada CRUD MongoDB. .NET terbukti unggul secara mutlak.
   Practical significance: Perbedaan sangat besar secara praktis. .NET menghasilkan throughput ~8.6x lebih tinggi (225.60 RPS vs 26.18 RPS) dan latency ~478x lebih cepat (4.64 ms vs 2218.66 ms) dibanding Spring Boot.
   Perbandingan literatur: Sejalan dengan Godinho et al. (2024) dan Grzeszuk & Miłosz (2025) yang mencatat efisiensi runtime .NET (CLR) dalam concurrency dan I/O bound tasks dibandingkan JVM.

5. Limitation:
   | Jenis | Ancaman | Dampak | Mitigasi |
   |-------|---------|--------|----------|
   | Internal | JVM Warm-up yang singkat | Overhead JIT compiler di awal run mempertinggi standard deviasi Spring Boot | Lakukan warmup lebih lama (>60s) atau gunakan compile AOT (Spring Native) |
   | External | Docker local deployment | Hasil tidak menggambarkan overhead network latency riil di cloud cluster | Lakukan pengujian di multi-node cloud environment (misal AWS EC2 + Atlas) |
   | Statistical| Ukuran sampel kecil (n=5) | Lebar confidence interval untuk latency Spring Boot cukup lebar (rentang ~1500ms) | Tingkatkan jumlah run eksperimen menjadi n=30 |

6. Failure Analysis (jika H₀ tidak ditolak):
   Penyebab potensial  : N/A (H₀ ditolak). Namun kegagalan Spring Boot menyamai performa .NET dianalisis sebagai akibat dari blocking I/O overhead dan GC pauses dalam docker resource limits yang ketat.
   Boundary condition   : N/A. Namun Spring Boot cenderung lebih stabil dalam hal error rate (23% vs 33%) karena membatasi laju request masuk (backpressure implisit akibat latency tinggi).
   Insight              : Kecepatan pemrosesan yang sangat tinggi pada .NET mendorong MongoDB ke batas kapasitasnya (saturasi resource), memicu connection pool exhaustion dan error rate lebih tinggi.
```

---

## Latihan 1 — Pemilihan Uji Statistik

Tentukan uji statistik yang tepat untuk eksperimen Anda.

| Pertanyaan | Jawaban |
|-----------|---------|
| Berapa grup yang dibandingkan? | 2 (Spring Boot vs .NET) |
| Apakah data berpasangan (paired)? | Tidak (Independent) |
| Apakah distribusi normal? (uji normalitas) | Melalui Shapiro-Wilk: Throughput normal (p_sb=0.1357, p_dn=0.5306). Latency tidak normal pada Spring Boot (p=0.0155). |
| **Uji yang dipilih:** | Independent t-test (untuk Throughput) dan Mann-Whitney U (untuk p95 Latency) |
| **Justifikasi:** | Throughput memenuhi semua asumsi parametrik (normalitas dan independensi). Latency melanggar asumsi normalitas pada data Spring Boot, sehingga memerlukan uji non-parametrik Mann-Whitney U. |

**Effect size yang akan dilaporkan:** [x] Cohen's d / [ ] Eta-squared / [ ] Lainnya: ____

---

## Latihan 2 — Interpretasi Hasil

Gunakan data berikut (atau data riil Anda) untuk berlatih interpretasi.

**Data:**
| Model | Accuracy (mean ± std) | n |
|-------|----------------------|---|
| A | 89.2 ± 1.5 | 10 |
| B | 87.8 ± 2.1 | 10 |

p = 0.045, Cohen's d = 0.74, CI 95% = [0.03, 2.77]

| Aspek | Interpretasi |
|-------|-------------|
| Signifikansi statistik | p < 0.05 (p=0.045) → Perbedaan performa antara Model A dan Model B signifikan secara statistik pada tingkat signifikansi α = 0.05. |
| Effect size | Cohen's d = 0.74 menunjukkan effect size berukuran sedang ke besar (medium-to-large), yang berarti terdapat perbedaan yang cukup substansial dalam distribusi populasi kedua model. |
| Practical significance | Perbedaan akurasi rata-rata sebesar 1.4% secara praktis bernilai tinggi untuk domain kritis seperti deteksi penyakit medis atau kendaraan otonom, di mana peningkatan kecil dapat menyelamatkan nyawa/mengurangi kesalahan fatal. |
| Hubungan ke RQ | Menjawab RQ dengan membuktikan bahwa Model A memiliki efektivitas akurasi yang lebih unggul dibandingkan dengan Model B. |
| Perbandingan literatur | Hasil ini memperkuat penelitian dari Zhao et al. (2023) yang menyatakan bahwa penambahan mekanisme attention (pada Model A) meningkatkan akurasi klasifikasi secara konsisten dibanding baseline (Model B). |

---

## Latihan 3 — Failure Analysis

Latih kemampuan failure analysis: hipotesis TIDAK didukung. Apa yang bisa dipelajari?

**Skenario:** Metode baru Anda mendapat F1 = 83.2%, baseline = 84.7%. p = 0.12 (tidak signifikan).

| Pertanyaan | Jawaban |
|-----------|---------|
| Apakah ini "gagal"? | Bukan gagal total — hipotesis tidak terdukung adalah temuan yang valid dan bisa menjadi kontribusi. |
| Kemungkinan penyebab? | Metode baru menambah kompleksitas komputasi (+40% waktu) tanpa peningkatan F1 yang cukup — overhead tidak sebanding. |
| Boundary condition? | Metode ini hanya efektif ketika data ≥ 10.000 record; di dataset kecil (<1.000), baseline lebih stabil. |
| Insight yang bisa diambil? | Ada trade-off ukuran data vs kompleksitas — rekomendasikan hybrid approach yang adaptif berdasarkan ukuran dataset. |
| Apakah layak dilaporkan? Mengapa? | Ya — negative result + boundary condition analysis adalah kontribusi riset yang diakui komunitas (ex: ACL, SIGIR). Mencegah riset duplikasi yang berulang. |

**Limitation terkait:**
| Jenis | Ancaman | Dampak |
|-------|---------|--------|
| *Contoh: Statistical* | *Contoh: Hanya 5 run per skenario* | *Power test rendah* |
| Internal | Durasi warm-up JVM terlalu pendek (30s) | JIT compilation overhead masuk ke dalam window steady-state |
| External | Resource limit container dibatasi ketat (2 vCPU, 2GB) | JVM mengalami throttling cpu lebih parah dibanding runtime native .NET |

---

## Refleksi

> Apakah "failure" dalam riset benar-benar gagal, atau justru kontribusi? Bagaimana failure analysis mengubah cara Anda melihat hasil negatif?

Dalam riset ilmiah, hasil negatif atau "kegagalan" menolak hipotesis nol ($H_0$) bukanlah suatu kegagalan pribadi atau riset yang sia-sia, melainkan sebuah kontribusi pengetahuan yang valid. Failure analysis mengubah cara pandang kita dengan menggeser fokus dari sekadar mencari pembuktian sukses ("hipotesis terbukti") menjadi pemahaman mendalam tentang batasan dan kondisi batas (boundary conditions) suatu sistem atau metode. 

Melaporkan hasil negatif secara transparan beserta analisis mengapa suatu metode tidak bekerja (misal akibat saturasi resource database atau garbage collection overhead) membantu komunitas ilmiah menghindari jalan buntu yang sama, menghemat sumber daya riset secara kolektif, dan membuka jalan bagi rancangan solusi hibrida yang lebih adaptif di masa depan. Kegagalan tanpa analisis barulah sebuah kegagalan sejati; namun kegagalan yang dianalisis secara mendalam adalah fondasi bagi penemuan ilmiah berikutnya.
