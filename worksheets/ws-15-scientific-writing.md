# WS-15: Scientific Writing

> **Bab 15 — Penulisan Ilmiah**

---

## Ringkasan Materi

### Scientific Argument Flow

```
Problem → Gap → RQ → Method → Result → Analysis → Conclusion → Contribution
```

Paper ilmiah adalah **satu argumen utuh** dari masalah ke kontribusi. Setiap node harus terhubung logis ke node sebelum dan sesudahnya.

### Struktur IMRAD

| Section | Peran | Pertanyaan Kunci |
|---------|-------|-----------------|
| **Introduction** | Motivasi + frame | Why is this needed? |
| **Method** | Deskripsi (reproducible) | How was it done? |
| **Results** | Laporan objektif | What was found? |
| **Discussion** | Interpretasi + refleksi | What does it mean? |
| **Conclusion** | Ringkasan + kontribusi | So wh
at? |

### Logical Flow — "Red Thread"

Setiap paragraf menjawab satu pertanyaan dan memicu pertanyaan berikutnya. Alur logis ini harus terasa di tiga level:
1. **Antar-kalimat** dalam paragraf
2. **Antar-paragraf** dalam section
3. **Antar-section** dalam paper

### Internal Consistency

Setiap elemen yang dijanjikan di Introduction harus hadir di Discussion/Conclusion.

**Consistency Matrix:**
```
           Intro  Method  Result  Discuss  Conclude
RQ1          ✓      ✓       ✓       ✓        ✓
RQ2          ✓      ✓       ✓       ✗ ←      ✓
Metrik-X     ✗      ✗       ✓ ←     ✗        ✗
```
**Masalah:** RQ2 dibahas di semua bagian kecuali Discussion. Metrik-X muncul di Result tapi tidak diperkenalkan di Method.

### Writing Quality Triad

| Kualitas | Deskripsi | Contoh Buruk → Baik |
|----------|----------|---------------------|
| **Clarity** | Dipahami sekali baca | "Performa meningkat" → "Accuracy meningkat dari 85.3% ke 89.7%" |
| **Precision** | Istilah eksak, tanpa ambiguitas | "signifikan" → "signifikan secara statistik (p=0.003, d=1.2)" |
| **Conciseness** | Setiap kata menambah informasi | Hapus kalimat redundan, filler words |

### Urutan Penulisan yang Disarankan

1. **Method & Results** — paling stabil, tulis pertama
2. **Discussion** — interpretasi berdasarkan hasil
3. **Introduction** — frame sesuai temuan aktual
4. **Abstract & Conclusion** — terakhir

### Target Jumlah Kata

| Section | Target |
|---------|--------|
| Introduction | 500–700 |
| Related Work | 700–1000 |
| Method | 800–1200 |
| Results | 500–800 |
| Discussion | 600–900 |
| Conclusion | 200–400 |

### Jebakan Kognitif

1. "Lebih panjang = lebih lengkap" → conciseness lebih berharga
2. "Introduction harus ditulis pertama" → justru ditulis terakhir
3. "Jargon teknis = lebih ilmiah" → clarity lebih penting
4. "Discussion = ringkasan Results" → Discussion = interpretasi + konteks

---

## Template A.15 — Paper Structure Checklist

```
PAPER STRUCTURE CHECKLIST

Title   : Analisis Komparatif Performa REST API Java Spring Boot vs .NET Core pada Operasi CRUD Database MongoDB
Target  : [x] Jurnal  [ ] Konferensi  [x] Laporan

Section Check:
  [x] Abstract — masalah, metode, hasil utama, kontribusi (max 250 kata)
  [x] Introduction — konteks → gap → RQ → kontribusi → struktur paper
  [x] Related Work — concept-centric, gap positioning
  [x] Method — reproducible: desain, variabel, metrik, setup, prosedur
  [x] Results — tabel + grafik + observasi (tanpa interpretasi)
  [x] Discussion — interpretasi, perbandingan, implikasi, limitation
  [x] Conclusion — jawaban RQ, kontribusi, future work

Consistency Matrix:
  [x] RQ di Introduction = RQ di Method = RQ di Conclusion
  [x] Variabel di Method = variabel di Results
  [x] Klaim di Discussion didukung data di Results
  [x] Limitasi di Discussion di-address di Conclusion/Future Work

Writing Quality:
  [x] Clarity — mudah dipahami tanpa re-read
  [x] Precision — tidak ada istilah ambigu
  [x] Conciseness — tidak ada kalimat redundan
```

---

## Latihan 1 — Paper Outline

Buat outline paper untuk riset Anda menggunakan struktur IMRAD.

| Section | Konten Utama (2-3 kalimat) | Target Kata |
|---------|---------------------------|------------|
| Abstract | Penelitian ini membandingkan kinerja Java Spring Boot vs .NET Core dalam penanganan REST API yang terhubung dengan database MongoDB di bawah batasan resource container (2 vCPU, 2GB RAM). Melalui 10 run eksperimental k6, metrik throughput dan p95 latency dikumpulkan. Hasil menunjukkan .NET memiliki throughput rata-rata ~8.6x lebih tinggi (225.60 RPS vs 26.18 RPS) dan p95 latency ~478x lebih cepat (4.64 ms vs 2218.66 ms) dibanding Spring Boot secara signifikan (p < 0.05). | 200-250 |
| Introduction | Konsep REST API yang efisien sangat krusial dalam arsitektur microservices modern yang dibatasi resource. Pemilihan framework backend sering kali didasarkan pada preferensi subyektif daripada bukti empiris kinerja. Studi ini bertujuan mengisi gap penelitian komparatif antara Spring Boot dan .NET Core menggunakan database NoSQL MongoDB dalam setup terkontrol ketat. | 500-700 |
| Related Work | Bagian ini mengulas literatur mengenai performa runtime JVM vs CLR, overhead garbage collection di lingkungan container, dan perbandingan I/O blocking vs non-blocking pada client driver database NoSQL. Mengidentifikasi gap dari studi terdahulu yang mayoritas menggunakan database relasional atau dataset tiruan berukuran kecil. | 700-1000 |
| Method | Eksperimen menggunakan rancangan comparison study terkontrol antara dua implementasi API yang identik fungsional. Pengujian beban dilakukan dengan k6 (50 Virtual Users, 120s steady-state) terhadap database MongoDB yang diisi 401.046 dokumen katalog produk IKEA. Pengujian normalitas data dilakukan dengan Shapiro-Wilk diikuti Independent t-test dan Mann-Whitney U untuk signifikansi statistik. | 800-1200 |
| Results | Menyajikan tabel hasil kuantitatif run 1-10 beserta visualisasi bar chart dan box plot untuk membandingkan metrik throughput (RPS), p95 latency (ms), dan error rate (%). Melaporkan hasil uji normalitas serta p-value dan effect size Cohen's d secara objektif tanpa interpretasi subjektif. | 500-800 |
| Discussion | Menganalisis keunggulan mutlak .NET yang didorong oleh efisiensi runtime CLR dalam concurrency I/O bound. Membedah latency Spring Boot yang sangat tinggi (>2 detik) akibat overhead warming-up JVM dan CPU throttling di docker. Menganalisis trade-off di mana throughput tinggi .NET memicu database saturation yang meningkatkan error rate (~33%) dibanding Spring Boot (~23%). | 600-900 |
| Conclusion | Menyimpulkan bahwa .NET Core memiliki kinerja throughput yang lebih tinggi dan p95 latency yang lebih rendah secara signifikan (p < 0.05, Cohen's d sangat besar) dibanding Spring Boot pada skenario CRUD MongoDB dengan resource container terbatas. Merekomendasikan penelitian lanjutan menggunakan Spring Native (AOT) dan konfigurasi pool koneksi dinamis. | 200-400 |

---

## Latihan 2 — Consistency Matrix

Buat consistency matrix untuk memverifikasi internal consistency paper Anda.

|  | Intro | Method | Result | Discussion | Conclusion |
|--|-------|--------|--------|-----------|-----------|
| RQ1 (Throughput) | ✓ | ✓ | ✓ | ✓ | ✓ |
| RQ2 (Latency) | ✓ | ✓ | ✓ | ✓ | ✓ |
| Metrik utama | ✓ | ✓ | ✓ | ✓ | ✓ |
| Variabel IV | ✓ | ✓ | ✓ | ✓ | ✓ |
| Variabel DV | ✓ | ✓ | ✓ | ✓ | ✓ |
| Klaim/kontribusi | ✓ | ✓ | ✓ | ✓ | ✓ |

**Isi setiap sel:** ✓ (ada & konsisten), ✗ (missing), ~ (ada tapi inkonsisten)

**Inkonsistensi yang ditemukan:**
> Tidak ditemukan inkonsistensi yang signifikan karena perencanaan di awal (UTS/WS-08) telah menetapkan metrik (throughput_rps dan p95_latency_ms) secara jelas, sehingga terminologi ini mengalir konsisten dari RQ di Introduction hingga draf Conclusion.

**Tindakan perbaikan:**
> Menjamin penulisan istilah metrik tetap konsisten (misal selalu menulis "p95 latency (ms)" dan bukan "kecepatan respon persentil ke-95") di seluruh naskah untuk menjaga integritas terminologi dan meminimalkan ambiguitas bagi pembaca.

---

## Latihan 3 — Writing Quality Check

Ambil satu paragraf dari tulisan Anda (atau tulis paragraf baru) dan evaluasi kualitasnya.

**Paragraf asli:**
> Eksperimen pengetesan performa REST API ini dicoba dengan software k6 untuk menguji backend Java Spring Boot dan .NET. Kita bisa melihat kalau hasil performa dari framework punya .NET itu lebih cepat daripada Java di database MongoDB. Hal ini disebabkan karena .NET punya garbage collection yang lebih bagus dan ramah di Docker limit CPU 2 dan memory 2GB sehingga nilainya signifikan sekali secara statistik.

| Kriteria | Evaluasi | Perbaikan |
|----------|---------|-----------|
| Clarity | Kalimat kedua menggunakan kata "lebih cepat" dan "hasil performa" yang ambigu — tidak jelas apakah yang dimaksud adalah throughput atau latency. | Ubah menjadi: "... .NET Core menghasilkan throughput yang lebih tinggi dan latency p95 yang lebih rendah dibanding Java Spring Boot..." |
| Precision | Pernyataan "signifikan sekali secara statistik" di kalimat ketiga tidak didukung oleh parameter statistik eksak (p-value, effect size). | Ubah menjadi: "...perbedaan tersebut signifikan secara statistik (p < 0.05) dengan effect size Cohen's d yang sangat besar (d > 5.0)." |
| Conciseness | Penggunaan kata "dicoba dengan", "Kita bisa melihat kalau", dan "framework punya .NET" merupakan wordiness informal yang memboroskan kata. | Ubah menjadi bentuk pasif formal ilmiah: "Pengujian performa REST API dilakukan menggunakan..." dan hilangkan filler words. |

**Paragraf setelah perbaikan:**
> Pengujian performa REST API Java Spring Boot dan .NET Core dilakukan menggunakan load-test generator k6 pada database MongoDB dengan pembatasan resource container (2 vCPU, 2GB RAM). Hasil analisis menunjukkan bahwa .NET Core menghasilkan throughput yang lebih tinggi dan latency p95 yang lebih rendah secara signifikan dibanding Java Spring Boot (p < 0.05, Cohen's d > 5.0). Perbedaan ini dipengaruhi oleh efisiensi manajemen memory runtime CLR .NET Core dalam menangani concurrent I/O tasks di bawah batasan resource CPU dan RAM container.

---

## Refleksi

> Apa perbedaan antara menulis "tentang" riset dan menulis sebagai "argumen" riset? Bagaimana urutan penulisan (Method → Discussion → Introduction) mengubah kualitas tulisan?

**Jawaban:**
> Menulis "tentang" riset bersifat deskriptif-kronologis (sekadar menceritakan kronologi aktivitas seperti: "kami membuat API, lalu kami mengujinya, lalu kami mencatat datanya"). Sebaliknya, menulis sebagai "argumen" riset berarti menyusun narasi logis terstruktur yang meyakinkan pembaca bahwa ada masalah nyata (Problem), ada celah di literatur (Gap), metode yang diajukan valid untuk menjawab masalah (Method), hasil eksperimen dapat dipercaya (Results), dan kesimpulannya memberikan kontribusi baru (Contribution). Setiap bagian menjadi premis yang saling mendukung untuk mempertahankan klaim utama paper secara utuh.
>
> Urutan penulisan Method -> Results -> Discussion -> Introduction -> Abstract mengubah kualitas tulisan secara dramatis karena membumikan argumen pada fakta eksperimental yang solid terlebih dahulu. Menulis bagian metodologi dan hasil di awal menjamin objektivitas data karena tidak dipengaruhi bias naratif pendahuluan. Setelah hasil terdefinisi dengan presisi, diskusi limitasi dan perbandingan literatur dapat dikembangkan secara proporsional. Akhirnya, pendahuluan (Introduction) ditulis untuk membingkai (frame) masalah secara akurat berdasarkan temuan riil, bukan berdasarkan ekspektasi awal yang mungkin meleset. Hal ini mencegah ketidakselarasan klaim (Red Thread) dan menjaga konsistensi logis internal draf naskah.
