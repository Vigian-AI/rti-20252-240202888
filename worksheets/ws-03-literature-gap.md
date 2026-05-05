# WS-03: Literature Mapping & Gap

> **Bab 3 — Literature Review, Research Gap & Baseline**

---

## Ringkasan Materi

### Literature Review = Positioning, Bukan Ringkasan

Literature review bukan merangkum paper satu per satu. Pendekatan yang benar adalah **concept-centric** — organisasi berdasarkan tema, metode, atau variabel. Tujuan: menemukan **pola, kontradiksi, dan gap**.

### Empat Jenis Research Gap

| Jenis Gap | Deskripsi | Contoh |
|-----------|----------|--------|
| **Performance Gap** | Performa belum memadai | Akurasi deteksi hanya 78% pada kasus tertentu |
| **Method Gap** | Pendekatan belum diterapkan | Belum ada yang pakai transformer untuk task ini |
| **Data Gap** | Dataset terbatas/tidak representatif | Semua studi pakai dataset sintetis |
| **Context Gap** | Belum diuji pada konteks berbeda | Belum ada evaluasi di negara berkembang |

Gap terkuat = kombinasi 2+ jenis.

### Systematic Search Strategy

1. **Database**: IEEE Xplore, ACM DL, Scopus, Google Scholar
2. **Boolean query** yang terdokumentasi eksplisit
3. **Snowballing**: backward (telusuri referensi) + forward (cari yang mengutip)
4. Klaim "belum ada penelitian" harus didukung **bukti pencarian**

### Baseline Selection — 3 Kriteria

| Kriteria | Pertanyaan |
|----------|-----------|
| **Relevan** | Apakah menyelesaikan masalah yang sama? |
| **Representatif** | Apakah mewakili common practice? |
| **State-of-the-Art** | Apakah terbaru/terbaik? |

Membandingkan deep learning 2024 dengan decision tree sederhana tanpa justifikasi = **straw man comparison** (perbandingan tidak jujur).

### Research vs Engineering

| Aspek | Engineering | Research |
|-------|------------|----------|
| Tujuan baca literatur | Mencari solusi yang sudah ada | Memahami apa yang belum terjawab |
| Cara membaca paper | Tutorial, how-to | Metode, limitasi, gap |
| Baseline | Framework terpopuler | State-of-the-art yang rigorous |
| Dokumentasi pencarian | Tidak diperlukan | Wajib (reproducible) |

### Istilah Penting

- **Concept-centric** — Organisasi literatur berdasarkan konsep/metode, bukan per penulis
- **Snowballing** — Backward (telusuri referensi) + Forward (cari yang mengutip paper kunci)
- **Research Position** — Pernyataan eksplisit posisi riset terhadap studi sebelumnya
- **Straw man comparison** — Memilih baseline lemah agar metode sendiri terlihat lebih baik

---

## Template A.3 — Literature Mapping & Gap Identification

```
LITERATURE MAPPING

Topik      : ____________________
Database   : ____________________
Query      : ____________________
Tahun      : ____________________
Hasil awal : ____ paper → Screening → ____ paper final

Literature Matrix (concept-centric):

| Study | Tahun | Method | Data | Result | Limitation |
|-------|-------|--------|------|--------|------------|
|       |       |        |      |        |            |

Pola yang ditemukan:
  Metode dominan     : ____________________
  Dataset umum       : ____________________
  Limitasi berulang  : ____________________

GAP IDENTIFICATION

Gap 1: [Jenis: performance / method / data / context]
  Deskripsi    : ____________________
  Bukti        : ____________________
  Signifikansi : ____________________

Gap 2: [Jenis: ____]
  Deskripsi    : ____________________
  Bukti        : ____________________
  Signifikansi : ____________________

Baseline Selection:
| Baseline | Relevansi | Representatif | Source |
|----------|-----------|---------------|--------|
|          |           |               |        |
```

---

## Latihan 1 — Concept-Centric Literature Table

Gunakan topik riset dari WS-02. Cari minimal 5 paper relevan menggunakan Google Scholar atau database lain.

**Topik riset:** Perbandingan Kinerja Framework Backend (Java Spring Boot vs .NET)
**Query pencarian:** "performance comparison" AND ("spring boot" OR "java") AND (".net core" OR "asp.net")
**Database:** Google Scholar, IEEE Xplore, ACM DL

| # | Study | Tahun | Method | Dataset | Result | Limitasi |
|---|-------|-------|--------|---------|--------|----------|
| 1 | Godinho et al. | 2024 | Benchmarking API (GET, POST, PUT, DELETE) pada dataset identik. | Data relasional (pelanggan, produk, pesanan) | .NET sedikit lebih unggul dalam response time, namun Spring Boot lebih stabil di bawah beban tinggi. | Hanya menguji pada satu jenis database (SQL). |
| 2 | Kronis & Uhanova | 2018 | Benchmarking REST service (JSON) di server terpisah. | Data JSON sederhana | ASP.NET Core (Kestrel) menunjukkan performa lebih baik daripada Java EE (TomEE) di lingkungan Linux. | Versi teknologi yang digunakan sudah usang (Java EE 7, .NET Core 2). |
| 3 | Sirigiri | 2023 | Review-driven assessment (studi literatur), bukan eksperimen langsung. | Agregasi dari studi lain | .NET Core unggul di startup time & memory, cocok untuk serverless. Spring Boot lebih baik untuk ekosistem enterprise. | Tidak ada data primer, hanya meta-analisis. |
| 4 | Hadiewijaya & Wasito | 2024 | Benchmarking algoritma binary search pada dataset berbeda ukuran. | 1 juta, 5 juta, 10 juta data (ID, Nama, Alamat) | C# lebih cepat untuk data kecil-sedang. Java lebih stabil untuk data besar karena optimasi JIT. | Fokus pada algoritma pencarian, bukan operasi API/CRUD. |
| 5 | Grzeszuk & Miłosz | 2025 | Analisis kinerja operasi CRUD dengan tool VisualVM & Postman. | Data relasional (PostgreSQL) | ASP.NET Core unggul pada task CPU-intensive. Spring Boot lebih stabil dalam penggunaan memori. | Tidak dijelaskan secara rinci skenario load testing yang digunakan. |

**Pola yang terlihat — Metode dominan:** Benchmarking eksperimental dengan membuat dua aplikasi identik untuk operasi CRUD atau REST API.
**Limitasi yang berulang:** Pengujian seringkali terbatas pada skenario spesifik (misalnya, satu jenis database, tanpa reverse proxy) dan versi teknologi yang cepat usang.

---

## Latihan 2 — Gap Identification

Berdasarkan tabel di Latihan 1, identifikasi gap.

| Jenis Gap | Ditemukan? | Gap Statement |
|-----------|-----------|---------------|
| Performance Gap | [x] Ya / [ ] Tidak | Sebagian besar studi menunjukkan .NET Core unggul dalam raw speed, namun Spring Boot lebih stabil. Belum ada yang mengukur trade-off antara throughput dan stabilitas memori secara kuantitatif. |
| Method Gap | [x] Ya / [ ] Tidak | Belum ada studi yang membandingkan performa dalam arsitektur yang lebih kompleks seperti microservices dengan service discovery dan API gateway, atau dalam konteks serverless (cold start). |
| Data Gap | [ ] Ya / [ ] Tidak | Dataset yang digunakan umumnya sintetis atau relasional sederhana. Belum ada perbandingan menggunakan database NoSQL (misal: MongoDB, Redis) yang umum di arsitektur modern. |
| Context Gap | [x] Ya / [ ] Tidak | Perbandingan sering dilakukan di lingkungan "steril" (dedicated server). Belum ada evaluasi performa di platform container orchestration seperti Kubernetes dengan skenario auto-scaling. |

**Gap utama yang dipilih:** Kombinasi Method, Data, dan Context Gap.
**Mengapa gap ini penting (bukan sekadar "belum ada yang meneliti")?**
> Teknologi cloud-native seperti Kubernetes, database NoSQL, dan arsitektur microservices bukan lagi hal baru, melainkan standar industri. Memilih framework hanya berdasarkan performa CRUD sederhana di server tunggal tidak lagi relevan. Pengembang perlu tahu bagaimana performa kedua framework dalam ekosistem modern yang realistis, termasuk bagaimana mereka berinteraksi dengan service mesh, seberapa cepat mereka scaling, dan bagaimana latensi berubah saat melintasi beberapa layanan. Jawaban atas pertanyaan ini memiliki dampak langsung pada biaya operasional, skalabilitas, dan keandalan sistem.

---

## Latihan 3 — Baseline Selection

Pilih 2 baseline dari literatur yang sudah dibaca.

| # | Baseline | Mengapa Relevan | Mengapa Representatif | Apakah SOTA? | Sumber |
|---|----------|----------------|----------------------|-------------|--------|
| 1 | Spring Boot | Task sama: membuat REST API. | Salah satu framework Java paling populer di industri untuk microservices. | Ya, masih menjadi standar de-facto di ekosistem Java. | Godinho et al. (2024), Sirigiri (2023) |
| 2 | .NET (Core) | Task sama: membuat REST API. | Pesaing utama Spring Boot dari ekosistem Microsoft, dengan adopsi yang terus meningkat. | Ya, merupakan framework modern dan performa tinggi dari Microsoft. | Godinho et al. (2024), Sirigiri (2023) |

**Apakah pemilihan baseline ini bisa dianggap straw man?** [ ] Ya / [x] Tidak
> Justifikasi: Tidak. Keduanya adalah teknologi modern, relevan, dan merupakan state-of-the-art di ekosistem masing-masing. Membandingkan keduanya adalah perbandingan yang adil dan relevan dengan pilihan yang dihadapi oleh para praktisi di industri saat ini. Ini bukan perbandingan dengan teknologi yang sudah usang atau jelas-jelas lebih lemah.

---

## Refleksi

> Apa perbedaan antara "belum ada yang meneliti ini" (klaim tanpa bukti) dengan research gap yang valid? Bagaimana cara membuktikan bahwa sebuah gap benar-benar ada?

**Jawaban:**
> Klaim "belum ada yang meneliti ini" adalah pernyataan kosong tanpa dasar. Sebaliknya, **research gap yang valid** adalah kesimpulan yang ditarik dari analisis sistematis terhadap literatur yang ada.
> Cara membuktikannya adalah dengan:
> 1. **Menunjukkan Bukti Pencarian (Systematic Search):** Mendokumentasikan query, database, dan jumlah paper yang di-screening (seperti pada tabel Literature Mapping). Ini membuktikan bahwa kita telah melakukan pencarian yang luas dan terstruktur.
> 2. **Menunjukkan Pola dan Batasan:** Meringkas apa yang **sudah** dilakukan oleh penelitian sebelumnya (pola metode, dataset, dll.) dan secara eksplisit menyatakan di mana batasan mereka berada (limitasi berulang).
> 3. **Mengartikulasikan "So What?":** Menjelaskan mengapa gap tersebut penting dan relevan untuk diisi, menghubungkannya dengan masalah praktis atau teoritis di dunia nyata, bukan hanya karena "kosong". Gap yang valid menunjukkan adanya pertanyaan penting yang belum terjawab oleh komunitas riset.
