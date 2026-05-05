# WS-05: Variabel & Metrik

> **Bab 5 — Metric, Measurement & Data**

---

## Ringkasan Materi

### Measurement Alignment Model

Setiap pengukuran yang valid harus bisa ditelusuri melalui rantai ini tanpa lompatan logis:

```
Problem → Concept → Variable → Metric → Data → Result
```

### Operationalization = Keputusan Desain

Menerjemahkan konsep abstrak menjadi variabel terukur bukan proses mekanis. "Code quality" yang diukur via SonarQube code smells membawa asumsi implisit. Setiap operasionalisasi harus didokumentasikan dan dijustifikasi.

### Empat Tipe Data (NOIR)

| Tipe | Ciri | Contoh | Operasi Valid |
|------|------|--------|---------------|
| **Nominal** | Kategori, tanpa urutan | Jenis algoritma (RF, SVM, CNN) | Modus, chi-square |
| **Ordinal** | Urutan, interval tidak sama | Skala Likert (1-5) | Median, Spearman |
| **Interval** | Jarak bermakna, tanpa nol absolut | Suhu Celsius | Mean, Pearson, t-test |
| **Ratio** | Jarak bermakna + nol absolut | Waktu eksekusi (ms) | Semua operasi |

Tipe data menentukan uji statistik yang valid. Kebanyakan metrik performa TI = ratio; persepsi pengguna = ordinal.

### Kriteria Pemilihan Metrik

- **Representative** — Mewakili konsep yang diteliti
- **Sensitive** — Cukup peka menangkap perbedaan bermakna (hindari ceiling effect)
- **Feasible** — Bisa dikumpulkan dalam batasan waktu dan biaya

### Pre-registration

Metrik harus ditentukan **sebelum** eksperimen. Memilih metrik setelah melihat data = **p-hacking**. Metrik tambahan yang ditemukan kemudian dilaporkan sebagai *exploratory*, bukan *confirmatory*.

### Primary vs Secondary Metric

- **Primary Metric** — Langsung terikat ke hipotesis, menentukan kesimpulan
- **Secondary Metric** — Pendukung, dilaporkan di samping primary; statusnya suplementer

### Research vs Engineering

| Aspek | Engineering | Research |
|-------|------------|----------|
| Pemilihan metrik | Berdasarkan kebiasaan/tool yang ada | Berdasarkan construct validity |
| Anomali | Dihapus untuk laporan bersih | Diinvestigasi — bisa jadi temuan |
| Kapan dipilih | Setelah sistem jadi (monitoring) | Sebelum eksperimen (by design) |

### Istilah Penting

- **Operationalization** — Transformasi konsep abstrak menjadi variabel terukur
- **Construct Validity** — Sejauh mana pengukuran benar-benar mengukur konsep yang dimaksud
- **Measurement Scale** — Klasifikasi data (NOIR) yang menentukan analisis valid
- **Multi-metric Evaluation** — Menggunakan beberapa metrik untuk menangkap konsep kompleks

---

## Template A.5 — Definisi Variabel, Metrik & Justifikasi

```
VARIABLE & METRIC DEFINITION

Research Question: ____________________

| Variabel | Tipe | Konsep | Metrik | Skala | Satuan | Cara Mengukur | Justifikasi |
|----------|------|--------|--------|-------|--------|---------------|-------------|
|          | IV   |        |        |       |        |               |             |
|          | DV   |        |        |       |        |               |             |
|          | CV   |        |        |       |        |               |             |

Alignment Check:
  RQ → Concept → Variable → Metric → Data → Result
  [ ] Setiap langkah terdokumentasi
  [ ] Tidak ada "lompatan logis"
  [ ] Metrik mengukur apa yang dimaksud (construct validity)
```

---

## Latihan 1 — Operationalization Chain

Gunakan RQ dari WS-04. Definisikan variabel dan metriknya.

**RQ:** Apakah terdapat perbedaan signifikan dalam **throughput (RPS)** dan **p95 latency (ms)** antara aplikasi REST API yang dibangun menggunakan **Java Spring Boot** dan **.NET** saat melakukan operasi CRUD pada database **MongoDB**?

| Variabel | Tipe | Konsep Abstrak | Metrik Konkret | Skala (NOIR) | Satuan |
|----------|------|---------------|----------------|-------------|--------|
| Framework backend | IV | Teknologi pengembangan backend | Kategori: Spring Boot vs .NET | Nominal | — |
| Throughput (primary) | DV | Kapasitas sistem menangani request | Requests per second (RPS), rata-rata pada steady-state | Ratio | requests/sec |
| p95 Latency (primary) | DV | Responsiveness (tail latency) | 95th percentile latency selama pengukuran | Ratio | ms |
| Dataset / DB config | CV | Ukuran dataset dan konfigurasi MongoDB | Fixed dataset seed, index config, instance sizing | — | — |
| Load profile / Env | CV | Skenario beban dan hardware | Virtual users, ramp-up, vCPU, RAM | Ratio / Nominal | users, cores, GB |

**Apakah ada lompatan logis dalam rantai?** [ ] Ya / [x] Tidak
> Semua langkah terdokumentasi: RQ menentukan framework (IV) dan metrik terukur (RPS, p95) yang dapat dikumpulkan dari load testing terhadap dua implementasi identik yang dijalankan di lingkungan yang dikontrol.

---

## Latihan 2 — Evaluasi Metrik

Evaluasi metrik DV yang dipilih di Latihan 1 menggunakan 3 kriteria.

Metrik primary: `Throughput (RPS)` dan `p95 Latency (ms)`.

| Kriteria | Metrik | Skor (1-5) | Justifikasi |
|----------|--------|-----------:|-------------|
| Representative | Throughput (RPS) | 5 | Langsung merepresentasikan kapasitas sistem di bawah beban; relevan untuk RQ comparison. |
| Sensitive | Throughput (RPS) | 4 | Peka terhadap perubahan performa, namun bisa saturasi pada batas hardware sehingga perlu pengaturan load yang tepat. |
| Feasible | Throughput (RPS) | 5 | Mudah dikumpulkan dengan tool load-testing (k6, JMeter, wrk). |
| Representative | p95 Latency (ms) | 5 | Menangkap pengalaman pengguna pada tail latency, sangat relevan untuk responsivitas. |
| Sensitive | p95 Latency (ms) | 5 | Peka terhadap perbedaan implementasi, terutama pada kondisi kontensi/garbage collection. |
| Feasible | p95 Latency (ms) | 4 | Dapat dikumpulkan namun membutuhkan banyak sampel dan stabilitas lingkungan untuk hasil konsisten. |

**Apakah perlu secondary metric?** [x] Ya
> Secondary metrics: CPU utilization, memory usage, error rate (5xx), request success rate, dan p99 latency. Alasan: membantu menjelaskan penyebab perbedaan (mis. bottleneck CPU, GC, atau error spikes) dan mencegah interpretasi melenceng jika primary metric dipengaruhi oleh faktor eksternal.

**Contoh kasus ceiling effect untuk metrik ini:**
> Jika beban yang diuji terlalu rendah dibanding kapasitas sistem, kedua framework dapat mencapai throughput maksimal yang sama dan latency sangat rendah sehingga perbedaan menjadi tidak terdeteksi (ceiling effect). Mitigasi: jalankan skenario dengan beberapa level beban termasuk near-saturation.

---

## Latihan 3 — Data Quality Check

Bayangkan data yang akan dikumpulkan dari eksperimen. Evaluasi 4 dimensi kualitas data.

Rancangan kualitas data untuk eksperimen perbandingan Spring Boot vs .NET:

| Dimensi | Pertanyaan | Jawaban | Strategi Mitigasi |
|---------|-----------|---------|------------------|
| Completeness | Apakah semua run dan metrik tercatat penuh? | Harus: setiap run menyimpan RPS, p95, p99, CPU, mem, error rate, dan konfigurasi lingkungan. | Otomasi pengumpulan (script + tool), simpan logs terstruktur (JSON), validasi post-run untuk deteksi data hilang; ulangi run jika ada missing. |
| Consistency | Apakah pengukuran konsisten antar-run dan antar-framework? | Risiko inkonsistensi jika environment tidak identik (background load, GC tuning). | Gunakan container/VM terstandardisasi, fix DB seed & config, disable background services, jalankan benchmark pada jam terkontrol; gunakan infra yang sama untuk kedua implementasi. |
| Validity | Apakah metrik benar mengukur konsep yang dimaksud? | Throughput dan p95 mengukur kapasitas dan pengalaman pengguna; namun butuh warm-up dan steady-state. | Definisikan prosedur pengukuran (warm-up period, steady-state window), dokumentasikan metric definitions, filter out startup/warmup samples. |
| Representativeness | Apakah skenario mewakili beban nyata target? | Bisa tidak mewakili jika beban sintetis terlalu sederhana. | Rancang beberapa workload profiles (light, medium, heavy, bursty), gunakan realistic request distributions and payloads, gunakan dataset yang menyerupai produksi. |

Tambahan praktik eksperimen:
- Lakukan minimal 30 pengulangan per kondisi jika memungkinkan, atau gunakan power analysis untuk menentukan jumlah run.
- Simpan metadata tiap run: commit hash, JVM/CLR version, OS, CPU, memory, MongoDB config, dataset seed, load profile.
- Gunakan alat monitoring (Prometheus/Grafana) untuk cross-check resource metrics.
- Tentukan prosedur analisis statistik (mis. t-test atau Wilcoxon) dan threshold effect size sebelum menjalankan eksperimen (pre-registration).

---

## Refleksi

> Mengapa memilih metrik setelah melihat data dianggap p-hacking? Apa bedanya dengan eksplorasi data yang sah?

**Jawaban:**
> Memilih metrik setelah melihat hasil memungkinkan peneliti memilih metrik yang menonjol untuk mendukung hipotesis (bias seleksi). Eksplorasi yang sah memisahkan analisis "confirmatory" (pre-registered, primary metrics) dan "exploratory" (post-hoc, dilaporkan terpisah), serta menyesuaikan klaim sesuai status temuan.
