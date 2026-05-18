# WS-07: Experimental Design & Validity

> **Bab 7 — Experimental Design & Validity**

---

## Ringkasan Materi

### Correlation ≠ Causality

Kausalitas membutuhkan 3 syarat:
1. **Covariance** — X dan Y bergerak bersama
2. **Temporal precedence** — X berubah sebelum Y
3. **Elimination of alternatives** — Tidak ada faktor lain yang menjelaskan Y

Controlled experiment adalah satu-satunya metode yang bisa membuktikan kausalitas.

### Empat Jenis Validitas

| Jenis | Pertanyaan | Ancaman Umum |
|-------|-----------|-------------|
| **Internal** | Apakah hubungan IV→DV nyata? | Confounding variable, selection bias |
| **External** | Apakah bisa digeneralisasi? | Dataset terlalu spesifik |
| **Construct** | Apakah mengukur konsep yang benar? | Metrik tidak sesuai |
| **Conclusion** | Apakah kesimpulan statistik valid? | Sample size kecil, uji salah |

Internal dan external validity sering berkonflik: semakin terkontrol (internal kuat) → semakin artificial (external lemah).

### Tiga Tipe Eksperimen dalam Riset TI

| Tipe | Deskripsi | Kapan Digunakan |
|------|----------|----------------|
| **Comparison Study** | Metode A vs B pada kondisi identik | Membandingkan pendekatan berbeda |
| **Ablation Study** | Full system → lepas komponen satu per satu | Mengukur kontribusi tiap komponen |
| **Parameter Study** | Variasikan satu parameter, amati dampak | Uji sensitifitas/robustness |

### Fairness dalam Perbandingan

Perbandingan yang adil = **kondisi identik** untuk semua metode: dataset sama, preprocessing sama, tuning effort sebanding, environment sama, metrik sama.

Contoh tidak adil: Transformer (30 fitur tambahan + Bayesian optimization) vs RF (default params) → hasilnya misleading.

### Threats to Validity = Diidentifikasi Sebelum Eksperimen

Ancaman validitas harus diidentifikasi **sebelum** eksperimen dan mitigasinya dirancang sebagai bagian dari desain — bukan ditulis sebagai boilerplate setelah selesai.

### Research vs Engineering

| Aspek | Engineering | Research |
|-------|------------|----------|
| Tujuan testing | Memastikan sistem memenuhi requirement | Membuktikan hubungan kausal antar variabel |
| Baseline | Versi sebelumnya (last release) | Metode tervalidasi dari literatur |
| Kegagalan | Bug → fix → release | H₀ tidak ditolak → tetap kontribusi ilmiah |
| Sukses | 100% test pass | Evidence valid — mendukung atau menolak hipotesis |

### Istilah Penting

- **Causality** — Hubungan sebab-akibat (covariance + temporal + elimination)
- **Controlled Experiment** — Ubah satu variabel, kontrol sisanya, amati efek
- **Fairness** — Semua metode diuji pada kondisi yang benar-benar identik
- **Threats to Validity** — Faktor yang bisa melemahkan kesimpulan jika tidak dimitigasi
- **Conclusion Validity** — Validitas statistik: power, sample size, uji yang tepat

---

## Template A.7 — Desain Eksperimen Lengkap

```
EXPERIMENT DESIGN

Research Question : Apakah terdapat perbedaan signifikan dalam throughput (RPS) dan p95 latency (ms) antara aplikasi REST API yang dibangun menggunakan Java Spring Boot dan .NET saat melakukan operasi CRUD pada database MongoDB?
Hypothesis        : H1 — Terdapat perbedaan signifikan pada throughput (RPS) dan p95 latency antara Spring Boot dan .NET pada kondisi eksperimen yang identik.
Tipe Eksperimen   : [x] Comparison  [ ] Ablation  [ ] Parameter

Kondisi Eksperimen:
| Kondisi | Deskripsi | IV Value | CV Settings |
|---------|-----------|----------|-------------|
| Control | Spring Boot API sebagai baseline pada skenario CRUD identik | Spring Boot | Dataset seed tetap, MongoDB config tetap, load profile tetap, vCPU/RAM/network identik |
| Treatment | .NET API identik secara fungsional pada skenario CRUD yang sama | .NET | Dataset seed tetap, MongoDB config tetap, load profile tetap, vCPU/RAM/network identik |

Fairness Checklist:
  [x] Dataset identik untuk semua kondisi
  [x] Preprocessing setara
  [x] Tuning effort setara
  [x] Environment identik
  [x] Metrik evaluasi sama

Threat Analysis:
| Threat Type | Ancaman Spesifik | Mitigasi |
|-------------|-----------------|----------|
| Internal    | Variasi runtime (JIT/GC), cache warm-up, dan noise resource | Warm-up terstandar, randomisasi urutan run, repeat N kali, clear cache antar-run |
| External    | Hasil mungkin hanya berlaku untuk dataset, MongoDB version, dan hardware tertentu | Uji pada variasi ukuran dataset dan minimal satu environment tambahan |
| Construct   | RPS/p95 mungkin tidak merepresentasikan kualitas layanan end-to-end | Tambahkan error rate dan p99 sebagai metrik pendukung, definisikan window steady-state |
| Conclusion  | Sample size kecil atau uji statistik tidak sesuai | Power analysis sederhana, gunakan uji non-parametrik jika distribusi tidak normal |

Statistical Plan:
  Uji statistik   : Shapiro-Wilk untuk normalitas; jika normal gunakan independent t-test, jika tidak gunakan Mann-Whitney U
  Justifikasi      : Dua kelompok independen dengan metrik numerik; pemilihan uji mengikuti distribusi data
  Alpha            : 0.05
  Effect size min  : Cohen's d >= 0.5 atau Cliff's delta >= 0.33
```

---

## Latihan 1 — Desain Eksperimen

Susun desain eksperimen berdasarkan RQ, variabel, dan sistem dari WS-04 sampai WS-06.

**RQ:** Apakah terdapat perbedaan signifikan dalam throughput (RPS) dan p95 latency (ms) antara aplikasi REST API yang dibangun menggunakan Java Spring Boot dan .NET saat melakukan operasi CRUD pada database MongoDB?
**Tipe eksperimen:** [x] Comparison / [ ] Ablation / [ ] Parameter

| Kondisi | Deskripsi | IV Value | CV Settings |
|---------|-----------|----------|-------------|
| Control | Spring Boot API sebagai baseline untuk skenario CRUD yang sama | Spring Boot | Dataset seed tetap, MongoDB config tetap, load profile tetap, vCPU/RAM/network identik |
| Treatment | .NET API identik secara fungsional | .NET | Dataset seed tetap, MongoDB config tetap, load profile tetap, vCPU/RAM/network identik |

---

## Latihan 2 — Fairness Checklist

Evaluasi apakah desain eksperimen di Latihan 1 sudah fair.

| Kriteria | Status | Detail |
|----------|--------|--------|
| Dataset identik | ✅ | Seed dataset, index, dan ukuran DB sama untuk semua run |
| Preprocessing setara | ✅ | Skema koleksi dan pipeline CRUD identik |
| Tuning effort setara | ✅ | Upaya tuning setara atau keduanya default dengan dokumentasi konfigurasi |
| Environment identik | ✅ | Container/VM sama, versi runtime dan MongoDB dipin |
| Metrik evaluasi sama | ✅ | RPS rata-rata steady-state dan p95 latency dari window yang sama |

**Ada yang tidak fair?** [ ] Ya / [x] Tidak
> Jika ya, bagaimana cara memperbaikinya? N/A

---

## Latihan 3 — Threat Analysis

Identifikasi ancaman validitas untuk desain eksperimen ini.

| Threat Type | Ancaman Spesifik | Mitigasi |
|-------------|-----------------|----------|
| Internal | Variasi performa karena warm-up JIT/GC dan cache | Standarisasi warm-up, randomisasi urutan eksperimen, ulangi N kali |
| External | Generalisasi terbatas pada satu dataset dan satu konfigurasi infra | Tambah variasi ukuran dataset dan satu konfigurasi infra lain |
| Construct | RPS/p95 saja belum cukup mewakili kualitas layanan | Tambahkan error rate, p99, dan CPU/memory sebagai metrik pendukung |
| Conclusion | Power statistik rendah jika run sedikit | Tentukan N minimal, laporkan CI dan effect size |

**Ancaman mana yang paling sulit dimitigasi?** External validity
**Mengapa?**
> Membutuhkan variasi environment dan dataset tambahan yang sering terbatas oleh resource dan waktu.

---

## Refleksi

> Sebuah paper melaporkan "metode kami mengalahkan semua baseline." Apa 3 pertanyaan pertama yang harus diajukan untuk mengevaluasi klaim ini?

**Jawaban:**
1. Apakah semua baseline diuji pada dataset, preprocessing, dan environment yang identik?
2. Apakah tuning effort dan konfigurasi baseline setara serta didokumentasikan dengan jelas?
3. Apakah hasilnya signifikan secara statistik dan disertai effect size/CI yang memadai?
