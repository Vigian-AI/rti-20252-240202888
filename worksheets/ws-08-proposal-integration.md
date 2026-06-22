# WS-08: Proposal Integration (UTS)

> **Bab 8 — Proposal & Checkpoint**

---

## Ringkasan Materi

### Proposal = Satu Argumen Utuh

Proposal riset bukan kumpulan bab yang independen. Ia adalah **satu argumen** yang mengalir dari masalah ke rencana solusi. Jika satu koneksi putus, seluruh proposal kehilangan koherensi.

### Integration Map — 6 Koneksi Kritis

```
Problem (Bab 2) → Gap (Bab 3) → RQ & H (Bab 4) → Metrik (Bab 5) → Sistem (Bab 6) → Eksperimen (Bab 7)
```

| Koneksi | Pertanyaan Verifikasi |
|---------|----------------------|
| Problem → Gap | Apakah gap muncul dari analisis literatur terhadap masalah? |
| Gap → RQ | Apakah RQ langsung menjawab gap yang teridentifikasi? |
| RQ → Metrik | Apakah setiap variabel di RQ punya metrik terdefinisi? |
| Metrik → Sistem | Apakah setiap metrik bisa diukur oleh komponen sistem? |
| Sistem → Eksperimen | Apakah desain eksperimen menggunakan sistem sebagai instrumen? |

### Koherensi Vertikal + Horizontal

- **Vertikal** — Alur logis atas-ke-bawah (problem → experiment). Setiap section menjawab pertanyaan yang diangkat section sebelumnya dan memunculkan pertanyaan baru.
- **Horizontal** — Konsistensi terminologi (nama variabel di RQ = di hipotesis = di metrik = di desain)

**Operasionalisasi Red Thread** (benang merah):
```
Bab 2 (Problem) → | memperkenalkan masalah X + evidensi |
                          ↓ menimbulkan pertanyaan: "apa akar gap-nya?"
Bab 3 (Gap)     → | menjawab pertanyaan tadi + membuka "lalu apa yang perlu diteliti?" |
                          ↓
Bab 4 (RQ/H)    → | menjawab gap dengan pertanyaan spesifik + prediksi terukur |
                          ↓
Bab 5-7 (Method)→ | menjawab RQ melalui desain eksperimen yang tepat |
```
Jika ada lompatan (section B tidak menjawab pertanyaan section A), red thread putus.

### Jebakan Kognitif

| Jebakan | Deskripsi |
|---------|----------|
| "Selling" Introduction | Menulis promosi, bukan menyajikan data dan gap |
| Copy-paste Methodology | Menyalin deskripsi tekstbook tanpa menyesuaikan ke RQ |
| Optimistic Timeline | Meremehkan waktu implementasi; selalu tambah buffer 30-50% |
| No Possibility of Failure | Mengimplikasikan hasil pasti sukses — proposal jujur mengakui H₀ mungkin tidak ditolak |

### Struktur Proposal

1. **Pendahuluan** — Latar belakang + problem statement (Bab 1-2)
2. **Tinjauan Pustaka** — Literature review + gap + baseline (Bab 3)
3. **RQ / Kontribusi / Hipotesis** — (Bab 4)
4. **Metodologi** — Metrik + sistem + desain eksperimen (Bab 5-7)
5. **Timeline & Output**

### Istilah Penting

- **Integration Map** — Diagram 6 koneksi kritis antar komponen proposal
- **Vertical Coherence** — Alur logis atas-ke-bawah
- **Horizontal Coherence** — Konsistensi terminologi di semua bagian
- **Checkpoint** — Titik self-assessment sebelum transisi dari desain ke eksekusi

---

## Template A.8 — Integration Checklist

```
PROPOSAL INTEGRATION CHECKLIST

Koneksi Vertikal (Flow Atas-Bawah):
  [ ] Problem → Gap: masalah terdokumentasi di literatur
  [ ] Gap → RQ: pertanyaan menjawab gap spesifik
  [ ] RQ → Hypothesis: hipotesis memprediksi jawaban
  [ ] Hypothesis → Metric: metrik mengukur variabel dalam hipotesis
  [ ] Metric → System: komponen sistem menghasilkan/mengukur metrik
  [ ] System → Experiment: desain eksperimen menggunakan sistem

Koneksi Horizontal (Konsistensi):
  [ ] Istilah sama di semua bagian
  [ ] Variabel di RQ = variabel di hipotesis = metrik di desain
  [ ] Scope tidak berubah dari masalah ke eksperimen

Cognitive Trap Checklist:
  [ ] Tidak ada paragraf "promosi" di pendahuluan (hanya data & gap)
  [ ] Metodologi disesuaikan ke RQ, bukan copy-paste textbook
  [ ] Timeline sudah ditambah buffer 30-50% dari estimasi awal
  [ ] Proposal mengakui kemungkinan H0 tidak ditolak (honest uncertainty)
  [ ] Tidak ada klaim "pasti berhasil" atau "meningkatkan signifikan"

Rubrik Self-Assessment:
| Kriteria     | 1 (Lemah)                                        | 2 (Cukup)                                     | 3 (Baik)                                           | Skor |
|------------- |--------------------------------------------------|-----------------------------------------------|----------------------------------------------------|------|
| Koherensi    | >2 koneksi vertikal terputus                     | 1-2 koneksi lemah, argumen masih bisa diikuti | Semua 6 koneksi terhubung, red thread jelas        |      |
| Specificity  | Variabel/metrik masih abstrak, tidak ada angka   | Sebagian metrik terdefinisi numerik           | Semua metrik + threshold + unit pengukuran jelas   |      |
| Feasibility  | Timeline >6 bulan tanpa memperhitungkan sumber   | Timeline 3-6 bulan dengan asumsi tertentu     | Timeline 1-3 bulan realistis dengan rencana detail |      |
| Rigor        | Baseline tidak jelas atau straw man              | 1-2 baseline dengan justifikasi partial       | 2+ baseline SOTA + justifikasi pemilihan lengkap   |      |
```

---

## Latihan 1 — Kompilasi Proposal Mini

Kumpulkan hasil dari WS-02 sampai WS-07 menjadi satu ringkasan proposal.

| Komponen | Sumber | Isi (1-2 kalimat) |
|----------|--------|-------------------|
| Problem Statement | WS-02 | Pemilihan framework backend (Spring Boot vs .NET) masih sering berbasis preferensi, meskipun bukti empiris menunjukkan variasi kinerja yang nyata. Belum ada mekanisme evaluasi yang secara eksplisit menimbang throughput dan latensi pada konteks database NoSQL (MongoDB) yang merupakan standar arsitektur modern. |
| Gap | WS-03 | Studi komparatif yang ada umumnya menggunakan database relasional, versi teknologi usang, atau environment uji yang terbatas — belum ada yang membandingkan Spring Boot vs .NET pada workload CRUD berbasis MongoDB dalam setup terkontrol dan terdokumentasi ketat (kombinasi method, data, dan context gap). |
| RQ | WS-04 | Apakah terdapat perbedaan signifikan dalam throughput (RPS) dan p95 latency (ms) antara aplikasi REST API yang dibangun menggunakan Java Spring Boot dan .NET saat melakukan operasi CRUD pada database MongoDB? |
| Hipotesis | WS-04 | H₁: Terdapat perbedaan signifikan secara statistik (>5%) dalam throughput dan p95 latency antara implementasi Spring Boot dan .NET pada kondisi eksperimen yang identik; H₀ menyatakan tidak ada perbedaan signifikan. |
| Variabel & Metrik | WS-05 | IV = framework backend (Spring Boot vs .NET, skala nominal); DV = throughput (RPS, ratio) dan p95 latency (ms, ratio); CV = dataset seed, konfigurasi MongoDB, load profile, vCPU/RAM/network. |
| Sistem | WS-06 | Dua implementasi REST API yang identik secara fungsional (Spring Boot dan .NET) terhubung ke satu instance MongoDB; load-test tool sebagai generator dan metrics collector sebagai pengukur DV; konfigurasi lingkungan dipin sebagai CV. |
| Desain Eksperimen | WS-07 | Comparison study terkontrol: control = Spring Boot API, treatment = .NET API, semua CV identik; fairness diverifikasi dengan checklist; analisis statistik menggunakan uji normalitas → independent t-test atau Mann-Whitney U, alpha 0.05, effect size Cohen's d ≥ 0.5. |

---

## Latihan 2 — Integration Checklist

Verifikasi 6 koneksi kritis. Isi dengan merujuk tabel di Latihan 1.

| Koneksi | Status | Bukti |
|---------|--------|-------|
| Problem → Gap | + | Problem (WS-02) mengidentifikasi tidak adanya evaluasi terukur; gap (WS-03) muncul dari analisis 5 paper yang menunjukkan semua studi menggunakan DB relasional atau environment terbatas, sehingga gap NoSQL/MongoDB terdokumentasi dari literatur. |
| Gap → RQ | + | Gap yang teridentifikasi adalah tidak adanya perbandingan Spring Boot vs .NET pada MongoDB; RQ (WS-04) langsung menanyakan perbedaan throughput dan p95 latency pada kondisi tersebut — pertanyaan menjawab gap secara spesifik. |
| RQ → Hypothesis | + | RQ menanyakan apakah ada perbedaan signifikan; H₁ (WS-04) memprediksi perbedaan >5% pada throughput dan p95 latency dengan threshold yang dijustifikasi (di bawah 5% dianggap noise eksperimental). |
| Hypothesis → Metric | + | H₁ menyebut throughput dan p95 latency; WS-05 mendefinisikan keduanya secara operasional (RPS rata-rata steady-state, persentil ke-95 latency dalam ms, skala ratio) dan menetapkan metrik sebelum eksperimen. |
| Metric → System | + | Throughput diukur oleh load-test collector; p95 latency diukur oleh response-time metrics collector — keduanya merupakan komponen eksplisit dalam mapping sistem WS-06. |
| System → Experiment | + | Desain eksperimen WS-07 menggunakan dua implementasi REST API dan pipeline load-test sebagai instrumen; kondisi control/treatment memetakan IV; seluruh CV dikunci sesuai komponen sistem. |

**Koneksi mana yang paling lemah?** Hypothesis → Metric
**Bagaimana cara memperkuatnya?**
> Threshold ">5%" perlu dijustifikasi lebih kuat dengan referensi literatur atau power analysis yang menentukan minimum detectable effect. Sebaiknya ditambahkan nilai numerik target (mis. RPS ≥ X atau latency ≤ Y ms) agar H₁ tidak hanya relasional tetapi juga absolut sebagai sanity check.

**Konsistensi horizontal — apakah istilah dan scope konsisten?** [x] Ya / [ ] Tidak
> Istilah "throughput (RPS)", "p95 latency (ms)", "Spring Boot", ".NET", dan "MongoDB" digunakan secara konsisten di seluruh WS-02 hingga WS-07 dan dalam proposal UTS. Scope tidak berubah: selalu fokus pada REST API dengan operasi CRUD pada MongoDB.

---

## Latihan 3 — Rubrik Self-Assessment

Evaluasi proposal mini menggunakan rubrik.

| Kriteria | Skor (1-3) | Justifikasi |
|----------|-----------|-------------|
| Koherensi | 3 | Semua 6 koneksi vertikal terhubung dan terdokumentasi. Red thread jelas: masalah pemilihan framework berbasis preferensi → gap NoSQL belum diteliti → RQ komparatif MongoDB → metrik throughput/latency → sistem dua API → eksperimen comparison terkontrol. |
| Specificity | 3 | Semua metrik terdefinisi numerik: throughput dalam RPS (rata-rata steady-state), p95 latency dalam ms, threshold signifikansi >5%, alpha 0.05, effect size Cohen's d ≥ 0.5. Unit pengukuran eksplisit di setiap tahap. |
| Feasibility | 2 | Dua implementasi REST API + satu instance MongoDB adalah setup yang realistis dalam 1-3 bulan. Namun jadwal di proposal UTS masih berupa kolom kosong tanpa alokasi minggu yang eksplisit — perlu diisi dengan buffer 30-50%. |
| Rigor | 3 | Dua baseline SOTA yang relevan dan representatif (Spring Boot dan .NET) dengan justifikasi pemilihan dari 5 paper (Godinho et al. 2024, Grzeszuk & Miłosz 2025, Kronis & Uhanova 2018, dll.). Perbandingan bukan straw man karena keduanya adalah framework modern aktif. |

**Skor total:** 11 / 12

**Apakah proposal siap untuk fase eksekusi?** [x] Ya / [ ] Belum
> Proposal memiliki koherensi vertikal penuh, metrik spesifik, baseline yang kuat, dan desain eksperimen yang fair. Satu hal yang perlu dilengkapi sebelum eksekusi adalah pengisian jadwal dengan alokasi waktu eksplisit per aktivitas (implementasi dua API, setup MongoDB, benchmarking, analisis statistik) beserta buffer 30-50% dari estimasi awal.

---

## Refleksi

> Dari seluruh proses WS-01 sampai WS-08, bagian mana yang paling mudah dan paling sulit? Mengapa? Apa yang akan dilakukan berbeda jika mengulang dari awal?

**Bagian termudah:** Kompilasi dan verifikasi integrasi (WS-08 ini) — karena pada titik ini semua komponen sudah terdefinisi dengan jelas, sehingga mengisi tabel dan memeriksa koneksi terasa seperti validasi akhir, bukan pekerjaan baru.

**Bagian tersulit:** Identifikasi gap dan pemilihan metrik (WS-03 dan WS-05) — WS-03 membutuhkan analisis kritis terhadap limitasi setiap paper dan sintesis ke gap statement yang bermakna, bukan sekadar daftar "belum ada yang meneliti." WS-05 membutuhkan keputusan desain eksplisit tentang operasionalisasi konsep abstrak ("kinerja") menjadi metrik terukur yang valid sebelum eksperimen dijalankan.

**Yang akan dilakukan berbeda:**
> Pertama, menentukan metrik dan threshold secara eksplisit (pre-registration) lebih awal, bahkan sebelum sistem selesai didesain — ini mencegah godaan untuk menyesuaikan metrik setelah melihat hasil awal. Kedua, membuat integration map sederhana (6 koneksi) sejak WS-04 sebagai "kompas" agar setiap keputusan di WS-05, WS-06, dan WS-07 bisa langsung dicek koherensinya, tidak hanya diverifikasi di akhir pada WS-08.
