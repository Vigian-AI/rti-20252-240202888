# WS-01: Distorsi & Paradigma

> **Bab 1 — Research Mindset in IT**

---

## Ringkasan Materi

### Research Trust Model

Pengetahuan ilmiah tidak muncul langsung dari kenyataan. Ia melewati **6 tahap transformasi** yang masing-masing rawan distorsi:

```
Reality → Data → Processing → Analysis → Inference → Knowledge
```

Etika mencegah distorsi yang disengaja (fabrikasi, cherry-picking). Validitas mendeteksi distorsi yang tidak disengaja (confounding variable, sampling bias).

### Tiga Jenis Validitas

| Jenis | Pertanyaan | Contoh Ancaman |
|-------|-----------|----------------|
| **Internal Validity** | Apakah hubungan kausal benar ada? | Confounding variable |
| **External Validity** | Apakah bisa digeneralisasi? | Dataset terlalu homogen |
| **Construct Validity** | Apakah mengukur hal yang benar? | Metrik tidak sesuai klaim |

### Paradigma Riset

Mata kuliah ini menggunakan pendekatan **Positivist** (fenomena TI bisa diukur objektif melalui eksperimen terkontrol) diperkuat **Design Science Research** (artefak dibuat sebagai instrumen pengujian hipotesis, bukan tujuan akhir).

### Mode Berpikir Peneliti

**Curious** (mempertanyakan fenomena) → **Critical** (mengevaluasi klaim berdasarkan bukti) → **Systematic** (merancang investigasi terstruktur dan reproducible).

### Research vs Engineering

| Aspek | Engineering | Research |
|-------|------------|----------|
| Tujuan | Membuat sistem yang bekerja | Menghasilkan pengetahuan yang valid |
| Pertanyaan khas | "Bagaimana membuatnya jalan?" | "Apakah klaim ini benar?" |
| Ukuran sukses | Sistem berfungsi, client puas | Hipotesis terjawab, temuan tervalidasi |
| Kegagalan | Harus dihindari | Harus dilaporkan (negative result = kontribusi) |

### Istilah Penting

- **Research Mindset** — Pola pikir yang menuntut bukti dan mempertanyakan asumsi
- **Research Ethics** — Prinsip perilaku: kejujuran, objektivitas, keterbukaan, akuntabilitas
- **HARKing** — Hypothesizing After Results are Known — merumuskan hipotesis setelah melihat data
- **Falsifiability** — Hipotesis harus bisa dibuktikan salah

---

## A.1 — Research Mindset Self-Assessment

```
Nama Peneliti    : Vigian Agus Isnaeni
Tanggal          : 12 April 2026

1. Ketika membaca klaim "metode X 95% akurat":
   - Pertanyaan pertama saya: Klaim "Swift lebih cepat dan lebih efisien" dihitung dari metrik apa, pada skenario apa, dan dibandingkan secara setara atau tidak?
   - Data yang dibutuhkan untuk verifikasi: Definisi metrik (baris kode, CPU, memori), prosedur pengukuran, perangkat uji, hasil per fitur, dan batasan studi.

2. Posisi paradigma:
   - Pendekatan: [ ] Positivis  [ ] Interpretivis  [ ] Design Science  [x] Mixed
   - Alasan: Paper mengukur hasil secara kuantitatif (baris kode, CPU, memori) dan sekaligus membangun artefak aplikasi iOS dari rancangan Android.

3. Identifikasi distorsi:
   - Asumsi tersembunyi: Baris kode yang lebih sedikit otomatis berarti pengembangan lebih cepat dan lebih baik.
   - Sumber bias potensial: Studi kasus hanya satu aplikasi (Bujang Kurir), perbedaan runtime Android dan iOS, serta perbedaan alat ukur di Android Studio dan Xcode.
   - Langkah mitigasi: Tambah sampel aplikasi lintas domain, samakan skenario pengujian, dan laporkan hasil dengan kontrol variabel yang lebih ketat.

4. Komitmen etika:
   - Data yang tidak akan dimanipulasi: Data mentah pengukuran CPU, memori, jumlah baris, termasuk hasil yang tidak mendukung hipotesis.
   - Batasan yang diakui sejak awal: Studi berbasis satu kasus dan periode teknologi tertentu, sehingga generalisasi ke semua aplikasi masih terbatas.
```

---

## Latihan 1 — Identifikasi Distorsi

Pilih satu paper riset di bidang TI yang mengklaim "metode X meningkatkan performa." Telusuri setiap tahap Research Trust Model.

**Paper yang dipilih:**
> Judul: Perbandingan Pemograman Swift dan Java pada Bujang Kurir
> Penulis (Tahun): Pandhe Prakarsa, M. Azhar Irwansyah, Helen Sastypratiwi (2020)

| Tahap | Apa yang Dilakukan | Potensi Distorsi |
|-------|-------------------|-----------------|
| Reality → Data | Menggunakan aplikasi Bujang Kurir sebagai studi kasus: Android (Java) yang sudah ada, lalu dibuat versi iOS (Swift). | Bias sampel karena hanya satu aplikasi dan satu domain layanan. |
| Data → Processing | Menghitung baris kode efektif dan mencatat performa CPU/memori menggunakan profiler Android Studio dan Xcode. | Risiko bias pengukuran karena definisi baris efektif bersifat operasional dan alat lintas platform tidak sepenuhnya sebanding. |
| Processing → Analysis | Membandingkan hasil per fitur (beranda, form makanan, keranjang) dan tren kenaikan penggunaan resource. | Risiko construct validity: baris kode dijadikan proksi kemudahan pengembangan, padahal belum tentu mewakili kompleksitas kerja nyata. |
| Analysis → Inference | Menarik simpulan bahwa Swift lebih ringkas, lebih cepat dikembangkan, dan lebih baik untuk resource. | Confounding variable: selisih hasil bisa dipengaruhi perbedaan platform/runtime, bukan hanya bahasa pemrograman. |
| Inference → Knowledge | Menyimpulkan rancangan Android dapat dipakai untuk implementasi iOS pada Bujang Kurir. | Over-generalisasi jika kesimpulan diterapkan ke semua jenis aplikasi tanpa replikasi. |

**Distorsi paling besar di tahap:** Analysis -> Inference

**Dua distorsi spesifik yang teridentifikasi:**
1. Distorsi confounding: perbedaan performa bisa berasal dari karakteristik runtime/platform Android dan iOS, bukan semata-mata Java vs Swift.
2. Distorsi generalisasi: hasil dari satu studi kasus (Bujang Kurir) belum tentu berlaku untuk aplikasi dengan domain dan kompleksitas berbeda.

---

## Latihan 2 — Analisis Kasus Etika

Skenario: Seorang peneliti menemukan bahwa jika 3 data point outlier dihapus, hasil eksperimennya menjadi signifikan. Dengan outlier, hasilnya tidak signifikan.

| Perspektif | Analisis |
|------------|---------|
| Kejujuran ilmiah | Kedua hasil wajib dilaporkan (dengan dan tanpa outlier), termasuk alasan metodologis jika outlier dikeluarkan. |
| Transparansi | Prosedur pembersihan data harus ditulis sebelum analisis utama, bukan setelah melihat hasil signifikan. |
| Peer review | Reviewer harus dapat menilai apakah penghapusan outlier valid secara statistik atau hanya upaya membuat hasil terlihat signifikan. |

**Keputusan akhir dan justifikasi:**
> Outlier tidak boleh dihapus secara sepihak. Keputusan yang etis adalah melaporkan dua skenario dan menempatkan analisis sensitivitas sebagai bagian hasil. Dengan cara ini, kesimpulan tetap jujur, dapat direplikasi, dan tidak terjebak cherry-picking.

---

## Latihan 3 — Posisi Paradigma

**Topik riset:** Perbandingan efisiensi pengembangan dan performa resource antara Swift iOS dan Java Android pada studi kasus Bujang Kurir.

| Kriteria | Positivis | Interpretivis | Design Science |
|----------|-----------|---------------|----------------|
| Kesesuaian dengan topik (1–5) | 5 | 2 | 4 |
| Jenis data yang dikumpulkan | Data terukur: jumlah baris kode, tren CPU, dan tren memori per fitur. | Data naratif: pengalaman developer, kemudahan implementasi, serta konteks tim dan perangkat. | Data artefak: implementasi aplikasi iOS berbasis rancangan Android untuk diuji langsung. |
| Limitasi paradigma | Sulit mengontrol semua variabel platform; hasil terlihat objektif tetapi tetap bisa dipengaruhi confounder. | Generalisasi rendah karena bergantung pada konteks subjek dan pengalaman tim. | Fokus pada artefak bisa menggeser fokus dari pengujian kausal yang ketat. |

**Paradigma yang dipilih:** Positivis (diperkuat perspektif Design Science)
**Alasan:** Topik ini menuntut pembandingan berbasis bukti terukur, namun juga memerlukan pembuktian implementasi lewat artefak aplikasi iOS.

---

## Refleksi

> Sebelum membaca materi ini, apakah pernah mempertanyakan klaim "95% akurat"? Setelah memahami rantai distorsi, pertanyaan apa yang sekarang akan diajukan saat membaca paper?

**Jawaban:**
> Sebelumnya saya cenderung menerima klaim performa sebagai fakta jika terlihat didukung angka. Setelah memahami rantai distorsi, saya lebih hati-hati pada proses perubahan data menjadi kesimpulan.
> Pertanyaan yang sekarang saya ajukan saat membaca paper ini: apakah perbedaan hasil benar karena bahasa pemrograman, bagaimana variabel perancu dikendalikan, dan sejauh mana temuan dari satu studi kasus bisa digeneralisasi.
