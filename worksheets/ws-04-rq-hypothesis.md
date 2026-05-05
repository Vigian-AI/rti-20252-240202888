# WS-04: Research Question & Hypothesis

> **Bab 4 — Research Question, Contribution & Hypothesis**

---

## Ringkasan Materi

### RQ Bukan Pertanyaan Biasa

Research Question yang baik secara implisit mengandung cetak biru eksperimen: subjek, baseline, metrik, domain, dataset.

| Kualitas | Contoh |
|----------|--------|
| **Buruk** | "Bagaimana pengaruh deep learning terhadap deteksi malware?" |
| **Baik** | "Apakah CNN menghasilkan F1-Score lebih tinggi dari RF pada CIC-MalMem-2022?" |

Perbedaan: RQ yang baik menyebutkan **metode spesifik**, **metrik terukur**, **baseline**, dan **dataset**.

### Tiga Jenis RQ

| Jenis | Pola | Kebutuhan |
|-------|------|-----------|
| **Comparison** | A vs B → mana lebih baik? | ≥ 2 metode, metrik sama |
| **Improvement** | A' vs A → modifikasi lebih baik? | Pre/post, bukti perbaikan |
| **Exploratory** | Faktor X₁...Xₙ → pengaruh terhadap Y? | Multi-variabel, korelasi/regresi |

### Contribution Statement

Tiga jenis kontribusi: **Improvement** (metode terbukti lebih baik), **Comparison** (perbandingan sistematis yang belum ada), **Novel Approach** (pendekatan baru). Kontribusi harus terhubung langsung dengan gap — kontribusi tanpa gap = klaim tanpa justifikasi.

### Hypothesis H₀ / H₁

- **H₀** (Null) = Tidak ada perbedaan signifikan — asumsi default, harus dibuktikan salah
- **H₁** (Alternative) = Ada perbedaan signifikan — diterima hanya jika H₀ ditolak
- Harus **falsifiable**, mengandung **metrik terukur**, dirumuskan **SEBELUM eksperimen**

### Rantai Operasionalisasi

```
RQ → Variable → Metric → Data → Analysis
```

Jika rantai ini tidak lengkap, RQ belum mature. Bi-directional: RQ yang tidak bisa jadi hipotesis testable harus direvisi mundur.

### Research vs Engineering

| Aspek | Engineering | Research |
|-------|------------|----------|
| Tujuan pertanyaan | Apa yang harus dibangun? | Apa yang harus dibuktikan? |
| Bentuk jawaban | Sistem yang berfungsi | Bukti empiris terukur |
| Sukses diukur oleh | User satisfaction, uptime | Signifikansi statistik, effect size |
| Jika gagal | Debug dan perbaiki | Laporkan, analisis mengapa |

### Istilah Penting

- **Research Question (RQ)** — Pertanyaan spesifik: variabel terukur + metrik + konteks
- **Contribution Statement** — Apa yang diketahui setelah riset selesai yang sebelumnya belum ada
- **H₀ / H₁** — Null vs Alternative Hypothesis
- **Falsifiability** — Kondisi hipotesis ditolak harus bisa didefinisikan sebelum eksperimen
- **Operationalization** — Proses mewujudkan konsep abstrak menjadi variabel terukur

---

## Template A.4 — RQ-Contribution-Hypothesis

```
RQ-CONTRIBUTION-HYPOTHESIS

Gap Statement  : ____________________

Research Question:
  Tipe         : [ ] Comparison  [ ] Improvement  [ ] Exploratory
  Formulasi    : ____________________
  Variabel IV  : ____________________
  Variabel DV  : ____________________
  Metrik       : ____________________
  Dataset      : ____________________
  Baseline     : ____________________

Quality Check RQ:
  [ ] Variabel spesifik
  [ ] Metrik jelas
  [ ] Baseline ada
  [ ] Konteks disebutkan
  [ ] Memerlukan eksperimen (bukan hanya survei literatur)

Contribution Statement:
  Apa yang baru diketahui : ____________________
  Jenis kontribusi        : [ ] Improvement  [ ] Comparison  [ ] Novel approach
  Gap yang diisi          : ____________________

Hypothesis Pair:
  H₀ : ____________________
  H₁ : ____________________
  Threshold              : ____________________
  Justifikasi threshold  : ____________________
```

---

## Latihan 1 — Dari Gap ke RQ

Gunakan gap yang ditemukan di WS-03. Transformasikan menjadi Research Question.

**Gap dari WS-03:** Belum ada studi yang membandingkan kinerja Spring Boot dan .NET pada workload yang menggunakan database NoSQL (seperti MongoDB), yang merupakan standar dalam arsitektur modern.

**RQ versi pertama (tulis bebas):**
> Bagaimana perbandingan performa Spring Boot vs .NET kalau pakai database NoSQL?

**Evaluasi RQ:**

| Komponen | Ada? | Isi |
|----------|------|-----|
| Metode spesifik | [x] Ya | Spring Boot vs .NET |
| Metrik terukur | [ ] Tidak | Performa belum spesifik (throughput, latency?) |
| Baseline | [x] Ya | Spring Boot dan .NET saling menjadi baseline |
| Dataset/konteks | [x] Ya | Database NoSQL |

**Tipe RQ:** [x] Comparison / [ ] Improvement / [ ] Exploratory

**RQ versi revisi (setelah evaluasi):**
> Apakah terdapat perbedaan signifikan dalam **throughput (RPS)** dan **p95 latency (ms)** antara aplikasi REST API yang dibangun menggunakan **Java Spring Boot** dan **.NET** saat melakukan operasi CRUD pada database **MongoDB**?

---

## Latihan 2 — Hypothesis Pair

Rumuskan pasangan hipotesis dari RQ di Latihan 1.

| Komponen | Isi |
|----------|-----|
| H₀ | Tidak ada perbedaan signifikan secara statistik (>5%) dalam metrik throughput dan p95 latency antara implementasi Spring Boot dan .NET saat berinteraksi dengan database MongoDB. |
| H₁ | Terdapat perbedaan signifikan secara statistik (>5%) dalam metrik throughput dan p95 latency antara implementasi Spring Boot dan .NET saat berinteraksi dengan database MongoDB. |
| Metrik | Throughput (requests per second), p95 Latency (milliseconds) |
| Threshold | Perbedaan > 5% dianggap signifikan |
| Justifikasi threshold | Perbedaan di bawah 5% dalam benchmark kinerja seringkali berada dalam rentang noise atau variabilitas eksperimental, sehingga tidak dianggap sebagai perbedaan yang praktis atau substansial. |

**Apakah hipotesis ini falsifiable?** [x] Ya / [ ] Tidak
> Bagaimana cara membuktikannya salah? Jika hasil eksperimen menunjukkan perbedaan rata-rata metrik antara kedua framework adalah 5% atau kurang, maka kita gagal menolak H₀, yang berarti hipotesis alternatif (H₁) tidak terbukti.

---

## Latihan 3 — Rantai Operasionalisasi

Lengkapi rantai dari RQ hingga metode analisis.

| Tahap | Isi |
|-------|-----|
| RQ | Apakah terdapat perbedaan signifikan dalam throughput dan p95 latency antara Spring Boot dan .NET saat melakukan operasi CRUD pada database MongoDB? |
| Variable (IV) | Framework backend (Java Spring Boot vs .NET) |
| Variable (DV) | Throughput (RPS), p95 Latency (ms) |
| Metric | Requests per second (RPS) dan milidetik (ms) |
| Data source | Hasil load testing (misalnya dari K6, JMeter) terhadap dua aplikasi identik yang terhubung ke database MongoDB dengan dataset yang sama. |
| Analysis method | Uji-t (t-test) statistik untuk membandingkan rata-rata dari dua kelompok (Spring Boot vs .NET) untuk setiap metrik (throughput dan latency). |

**Apakah rantai lengkap?** [x] Ya / [ ] Tidak
> Jika tidak, tahap mana yang perlu direvisi? ______________

---

## Refleksi

> Ambil satu judul skripsi/paper yang pernah dibaca. Coba ekstrak RQ-nya. Apakah RQ tersebut memenuhi semua komponen (metode, metrik, baseline, konteks)? Jika tidak, apa yang hilang?

**Judul:** Perbandingan Performa Kinerja Node.js, PHP, dan Python dalam Aplikasi REST
**RQ yang diekstrak:** Bagaimana perbandingan performa (kecepatan respon, penggunaan CPU, penggunaan RAM) antara Node.js, PHP, dan Python dalam konteks aplikasi REST?
**Komponen yang hilang:**
- **Metrik Kurang Spesifik:** "Kecepatan respon" bisa lebih diperjelas (misalnya, rata-rata, p95, p99 latency).
- **Konteks Versi:** Paper menggunakan versi teknologi yang sudah usang (PHP 7.0, Python 2.7, Node.js 6), sehingga relevansinya untuk kondisi saat ini berkurang.
- **Konteks Beban Kerja:** Tidak dijelaskan secara rinci skenario *load testing* (misalnya, jumlah pengguna virtual, durasi, *ramp-up period*), hanya menyebutkan "10000 request pada saat yang bersamaan".
- **Baseline Implisit:** Ketiga bahasa saling menjadi baseline, yang sudah cukup baik, namun tidak dibandingkan dengan SOTA (State-of-the-Art) atau pendekatan lain yang mungkin lebih modern.
