# WS-02: Problem Statement

> **Bab 2 — Problem Formulation & System Context**

---

## Ringkasan Materi

### Problem Formation Model

Masalah riset melewati 5 tahap transformasi. Melompat langsung dari Reality ke Variable adalah kesalahan paling umum.

```
Reality → Observed Issue (Symptom) → Diagnosed Problem (Root Cause)
→ Researchable Problem (Scoped) → Measurable Variable (Operationalized)
```

### Topic ≠ Problem ≠ Research Problem

| Level | Contoh | Status |
|-------|--------|--------|
| **Topik** | Keamanan IoT | Terlalu luas, tidak bisa diuji |
| **Problem** | MQTT tidak terenkripsi | Spesifik tapi belum riset |
| **Research Problem** | Belum ada studi membandingkan overhead TLS 1.3 vs DTLS pada MQTT di IoT RAM < 64KB | Bisa dirancang eksperimennya |

### Symptom vs Root Cause

Apa yang diamati (gejala) ≠ mengapa terjadi (akar masalah). Gunakan **5 Whys** atau **Fishbone Diagram** untuk menggali.

Contoh: "User meninggalkan checkout" (symptom) → "Waktu loading > 8 detik karena API call sequential" (root cause).

### System Thinking

Setiap masalah riset TI harus terikat pada komponen sistem: **Input → Process → Output → Outcome → Constraints → Stakeholders**.

### Problem Quality Check

Masalah riset yang layak harus memenuhi 5 kriteria:
- **Clarity** — Satu orang membaca akan paham
- **Measurability** — Ada metrik kuantitatif
- **Relevance** — Penting untuk domain
- **Testability** — Bisa gagal (falsifiable)
- **Impact** — Ada kontribusi jika terjawab

### Research vs Engineering

| Aspek | Engineering | Research |
|-------|------------|----------|
| Tujuan | Menyelesaikan masalah (*solve*) | Memahami dan membuktikan (*understand & prove*) |
| Masalah | Bug, error, fitur belum ada | Gap dalam pengetahuan |
| Scope | Selesaikan semua yang perlu | Batasi agar bisa dibuktikan |
| Output | Working system | Evidence, paper, replicable findings |

### Istilah Penting

- **Problem Statement** — Formulasi tertulis: konteks sistem + gap + dampak + justifikasi
- **System Context** — Deskripsi lengkap: input, proses, output, outcome, constraints, stakeholders
- **Problem Drift** — Masalah "bermutasi" dari pendahuluan ke metodologi karena statement awal tidak presisi
- **Solution-First Thinking** — Memulai dari solusi tanpa masalah yang jelas — berbahaya dalam riset
- **Operational Definition** — Definisi variabel yang cukup jelas agar peneliti lain bisa mengukur hal yang sama

---

## Template A.2 — Problem Statement Builder

```
PROBLEM STATEMENT BUILDER

Domain & Konteks
  Domain   : Rekayasa Perangkat Lunak / Pengembangan Aplikasi Desktop
  Konteks  : Pemilihan bahasa pemrograman (Python, Java, C++, C#) dengan trade-off performa vs kemudahan pengembangan

System Context
  Input       : Kode program uji seragam untuk 3 skenario (komputasi intensif, pengolahan file besar, GUI dasar) pada empat bahasa
  Process     : Kompilasi/eksekusi pada lingkungan yang sama, lalu pengukuran waktu eksekusi, penggunaan memori, waktu kompilasi, dan jumlah baris kode
  Output      : Tabel komparatif metrik performa tiap bahasa
  Outcome     : Dasar pemilihan bahasa pemrograman desktop yang lebih objektif sesuai prioritas proyek
  Constraints : Satu mesin uji (Intel Core i5, RAM 8GB, SSD 256GB, Windows 11), tiga kali pengulangan, skenario uji terbatas
  Stakeholders: Developer desktop, technical lead, manajer proyek, dosen/mahasiswa TI

Fenomena → Problem
  Fenomena yang diamati             : Bahasa pemrograman populer menunjukkan karakteristik berbeda pada performa dan produktivitas pengembangan
  Gejala (symptom) yang terukur     : Pada hasil paper, waktu eksekusi bervariasi 120-290 ms; memori 15-50 MB; kompilasi 300-500 ms; baris kode 70-90
  Masalah yang didiagnosis          : Keputusan pemilihan bahasa sering belum berbasis kerangka evaluasi multi-kriteria yang terukur
  Masalah riset (researchable)      : Bagaimana pengaruh pilihan bahasa (Python, Java, C++, C#) terhadap performa runtime dan effort pengembangan pada skenario desktop seragam, serta trade-off mana yang paling sesuai untuk prioritas proyek yang berbeda?
  Variabel yang terukur             : Variabel bebas = bahasa pemrograman; variabel terikat = waktu eksekusi, memori, waktu kompilasi, jumlah baris kode; variabel kontrol = hardware, OS, skenario uji, jumlah pengulangan

Problem Quality Check
  [x] Clarity — Apakah satu orang membaca akan paham?
  [x] Measurability — Apakah ada metrik kuantitatif?
  [x] Relevance — Apakah penting untuk domain?
  [x] Testability — Apakah bisa gagal?
  [x] Impact — Apakah ada kontribusi jika terjawab?

Problem Statement (1 paragraf):
  Dalam konteks pengembangan aplikasi desktop, pemilihan bahasa pemrograman masih sering dilakukan berdasarkan kebiasaan tim, padahal hasil pengujian menunjukkan perbedaan kuantitatif yang nyata antarbahasa (waktu eksekusi 120-290 ms, penggunaan memori 15-50 MB, waktu kompilasi 300-500 ms, dan jumlah baris kode 70-90). Masalah risetnya adalah belum jelas bagaimana trade-off antara performa teknis dan kemudahan pengembangan dapat dievaluasi secara sistematis pada kondisi uji yang setara untuk Python, Java, C++, dan C#. Karena itu, penelitian difokuskan pada pengukuran komparatif empat metrik utama tersebut agar dapat menghasilkan dasar keputusan yang lebih objektif dalam memilih bahasa sesuai prioritas proyek desktop.
```

---

## Latihan 1 — Dari Topik ke Masalah Riset

Pilih satu topik di bidang TI yang diminati. Transformasikan melalui 5 tahap Problem Formation Model.

**Topik awal:** Analisis perbandingan performa bahasa pemrograman populer (Python, Java, C++, C#) dalam pengembangan aplikasi desktop.

| Tahap | Hasil |
|-------|-------|
| Reality | Dalam proyek desktop, tim perlu memilih bahasa yang memengaruhi performa aplikasi sekaligus kecepatan pengembangan. |
| Observed Issue (Symptom) | Data benchmark menunjukkan variasi besar antarbahasa: eksekusi 120-290 ms, memori 15-50 MB, kompilasi 300-500 ms, dan baris kode 70-90. |
| Diagnosed Problem (Root Cause) | Belum ada mekanisme keputusan yang secara eksplisit menimbang performa teknis dan effort coding berdasarkan kebutuhan proyek. |
| Researchable Problem | Belum diketahui bahasa mana yang paling sesuai untuk prioritas proyek desktop berbeda (mis. efisiensi runtime vs rapid development) pada lingkungan uji yang seragam. |
| Measurable Variable | Bahasa pemrograman; waktu eksekusi (ms); penggunaan memori (MB); waktu kompilasi (ms); jumlah baris kode; bobot prioritas kebutuhan proyek. |

**Apakah terjebak solution-first thinking?** [ ] Ya / [x] Tidak
> Jika ya, kembali ke tahap mana? -

---

## Latihan 2 — System Context Decomposition

Gambarkan konteks sistem dari masalah riset di Latihan 1.

| Komponen | Deskripsi |
|----------|----------|
| Input | Program uji setara pada Python, Java, C++, C# untuk tiga skenario: komputasi intensif, file I/O besar, dan GUI dasar. |
| Process | Kompilasi (untuk Java/C++/C#), eksekusi program, profiling performa, dan pencatatan metrik dengan prosedur yang sama. |
| Output | Nilai rata-rata waktu eksekusi, penggunaan memori, waktu kompilasi, serta jumlah baris kode tiap bahasa. |
| Outcome | Rekomendasi bahasa yang paling sesuai dengan karakteristik proyek desktop (fokus performa, keseimbangan, atau kecepatan development). |
| Constraints | Lingkungan uji tunggal, jumlah pengulangan terbatas, dan cakupan skenario yang belum merepresentasikan semua tipe aplikasi desktop. |
| Stakeholders | Pengembang software, tim engineering, project manager, institusi pendidikan TI, dan peneliti komparasi bahasa. |

**Komponen mana yang paling relevan dengan masalah riset?** Process (karena validitas kesimpulan sangat ditentukan oleh kesetaraan prosedur pengujian dan kontrol variabel).

---

## Latihan 3 — Problem Quality Check

Evaluasi problem statement yang sudah dibuat menggunakan 5 kriteria.

| Kriteria | Skor (1-5) | Justifikasi |
|----------|-----------|-------------|
| Clarity | 5 | Problem statement menyebut domain, konteks desktop, bahasa yang dibandingkan, dan arah analisis trade-off secara jelas. |
| Measurability | 5 | Semua variabel operasional terdefinisi kuantitatif: waktu eksekusi, memori, kompilasi, dan baris kode. |
| Relevance | 4 | Relevan untuk praktik pengembangan desktop, tetapi fokusnya belum mencakup konteks web/mobile. |
| Testability | 4 | Klaim dapat diuji dan berpotensi dibantah, namun masih berisiko confounder jika kontrol eksperimen kurang ketat. |
| Impact | 4 | Memberikan dasar keputusan teknis yang praktis, walau generalisasi lintas domain aplikasi masih terbatas. |

**Skor total:** 22 / 25

**Problem statement versi final (1 paragraf):**
> Pada pengembangan aplikasi desktop, pemilihan bahasa pemrograman masih kerap mengandalkan preferensi, meskipun bukti empiris menunjukkan perbedaan performa yang berarti antara Python, Java, C++, dan C#. Gejala ini terlihat dari variasi hasil uji pada metrik inti (waktu eksekusi, penggunaan memori, waktu kompilasi, dan jumlah baris kode), yang menandakan adanya trade-off nyata antara efisiensi runtime dan kemudahan pengembangan. Masalah riset yang diajukan adalah bagaimana mengevaluasi trade-off tersebut secara terukur pada skenario uji yang setara agar dapat ditentukan rekomendasi bahasa yang sesuai dengan prioritas proyek desktop. Dengan demikian, kontribusi riset diarahkan pada penyediaan dasar pengambilan keputusan yang lebih objektif, teruji, dan dapat direplikasi.

---

## Refleksi

> Bandingkan "masalah" yang biasa ditemui saat coding (bug, error) dengan masalah riset. Apa perbedaan fundamental dalam cara mendefinisikan dan mendekati keduanya?

**Jawaban:**
> Masalah saat coding biasanya bersifat lokal dan langsung operasional, seperti error sintaks, bug logika, atau fitur yang belum jalan; targetnya adalah memperbaiki sistem agar berfungsi. Sebaliknya, masalah riset adalah gap pengetahuan yang harus didefinisikan dengan batasan jelas, variabel terukur, dan desain uji yang dapat memvalidasi atau menolak klaim.
> Jadi pendekatan coding berfokus pada solusi cepat dan benar secara fungsional, sedangkan pendekatan riset berfokus pada pembuktian yang sistematis, transparan, dan dapat direplikasi oleh peneliti lain.
