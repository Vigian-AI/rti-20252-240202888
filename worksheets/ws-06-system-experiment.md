# WS-06: System-Experiment Mapping

> **Bab 6 — System Design sebagai Experimental Artifact**

---

## Ringkasan Materi

### Sistem = Instrumen Pengujian, Bukan Produk

Seorang engineer bertanya "apakah sistem bekerja?" — seorang peneliti bertanya "apa yang bisa dibuktikan sistem ini?" Sistem dalam riset adalah **artifact** — objek yang sengaja dibuat untuk menguji klaim spesifik.

### System as Experiment Model

```
RQ → Variable → System Component → Experimental Setup → Output
```

Setiap komponen sistem harus bisa ditelusuri ke variabel riset (top-down), dan setiap pengukuran harus menjawab RQ (bottom-up).

### Mapping Variabel ke Komponen

| Tipe Variabel | Peran di Sistem | Contoh |
|---------------|----------------|--------|
| **IV** (Independent) | Modul yang bisa di-toggle/swap | Algoritma A vs B |
| **DV** (Dependent) | Modul pengukuran | Logger, metrics collector |
| **CV** (Control) | Config yang dikunci | Dataset, parameter tetap |

Jika variabel tidak bisa di-map ke komponen apapun → arsitektur perlu didesain ulang.

### 4 Prinsip Desain Eksperimental

| Prinsip | Pertanyaan Kunci |
|---------|-----------------|
| **Traceability** | Komponen ini melayani variabel yang mana? |
| **Modularity** | Bisakah IV diubah tanpa memengaruhi yang lain? |
| **Controllability** | Apakah CV dieksternalisasi ke config file? |
| **Measurability** | Apakah sistem otomatis menghasilkan data yang dibutuhkan? |

### Variable Isolation melalui Arsitektur

- **Modular architecture** — Pisahkan berdasarkan variabel
- **Configuration-driven** — Ubah config (YAML/JSON), bukan code
- **Feature toggles** — On/off flag untuk ablation study

### Research vs Engineering

| Aspek | Engineering | Research |
|-------|------------|----------|
| Tujuan sistem | Memenuhi kebutuhan user | Menguji hipotesis, menghasilkan bukti |
| Arsitektur | Optimasi performa & skalabilitas | Optimasi isolasi variabel & reprodusibilitas |
| Konfigurasi | Sering hardcoded | Dieksternalisasi ke config file |
| Fitur tambahan | Menambah nilai user | Menambah noise jika tidak terkait RQ |

### Istilah Penting

- **Artifact** — Objek yang sengaja dibuat untuk memecahkan masalah atau menguji proposisi
- **Traceability** — Kemampuan menelusuri hubungan RQ → variabel → komponen → output
- **Variable Isolation** — Mengubah hanya satu variabel sambil menahan yang lain konstan
- **Ablation Study** — Menguji kontribusi tiap komponen dengan melepasnya satu per satu
- **Configuration-driven Execution** — Semua parameter di config file, bukan hardcoded

---

## Template A.6 — Mapping RQ ke Arsitektur Sistem

```
SYSTEM-EXPERIMENT MAPPING

Research Question: Apakah terdapat perbedaan signifikan dalam throughput (RPS) dan p95 latency (ms) antara aplikasi REST API yang dibangun menggunakan Java Spring Boot dan .NET saat melakukan operasi CRUD pada database MongoDB?

Variable → Component Mapping:
| Variabel | Tipe | Komponen Sistem | Cara Manipulasi/Pengukuran |
|----------|------|-----------------|---------------------------|
| Framework backend | IV   | Dua implementasi REST API yang identik secara fungsional: Spring Boot API dan .NET API | Ubah implementasi melalui config/deployment target, lalu bandingkan hasil load test |
| Throughput (RPS) | DV   | Load-test collector dan result aggregator | Ukur RPS rata-rata pada steady-state dari tool load testing |
| p95 latency | DV   | Metrics collector / logger respons | Ukur latency persentil ke-95 dari semua request selama window pengukuran |
| Dataset / DB config | CV   | MongoDB instance, dataset seed, index, dan skema koleksi | Kunci seed dataset, index, dan sizing instance agar tetap sama di semua run |
| Load profile / Env | CV   | Load generator, container/VM runtime, CPU, RAM, dan network setup | Tetapkan virtual users, ramp-up, vCPU, RAM, serta lingkungan eksekusi yang identik |

4 Prinsip Desain:
  [x] Traceability — Setiap komponen bisa ditelusuri ke variabel
  [x] Variable Isolation — IV bisa diubah tanpa mengubah CV
  [x] Measurement Integration — Pengukuran DV built-in
  [x] Reproducibility — Setup bisa direkonstruksi

Experimental Setup:
  Input data     : Dataset CRUD yang sama pada MongoDB dengan seed dan index tetap
  Parameter      : Framework backend, virtual users, ramp-up, vCPU, RAM, dan window steady-state
  Output format  : JSON/CSV berisi RPS, p95 latency, CPU, memory, error rate, dan metadata run
```

---

## Latihan 1 — Variable-to-Component Mapping

Gunakan RQ dan variabel dari WS-05. Petakan ke komponen sistem.

**RQ:** Apakah terdapat perbedaan signifikan dalam throughput (RPS) dan p95 latency (ms) antara aplikasi REST API yang dibangun menggunakan Java Spring Boot dan .NET saat melakukan operasi CRUD pada database MongoDB?

| Variabel | Tipe | Komponen Sistem | Cara Manipulasi / Pengukuran |
|----------|------|-----------------|---------------------------|
| Framework backend | IV | Dua implementasi REST API (Spring Boot dan .NET) | Deploy versi yang berbeda lalu jalankan benchmark yang sama |
| Throughput (RPS) | DV | Load-test results collector | Ambil rata-rata RPS pada steady-state dari hasil benchmark |
| p95 latency | DV | Response-time metrics collector | Hitung latency persentil 95 dari semua request valid |
| Dataset / DB config | CV | MongoDB instance dan dataset seed | Kunci isi dataset, index, dan konfigurasi DB untuk semua run |
| Load profile / Env | CV | Load generator dan infrastruktur eksekusi | Tetapkan virtual users, ramp-up, CPU, RAM, dan parameter lingkungan |

**Apakah semua variabel bisa di-map?** [x] Ya / [ ] Tidak
> Jika tidak, komponen apa yang perlu ditambahkan? N/A

---

## Latihan 2 — 4 Prinsip Desain

Evaluasi desain sistem terhadap 4 prinsip.

| Prinsip | Status | Bukti / Penjelasan |
|---------|--------|-------------------|
| Traceability | ✅ — setiap komponen utama dapat ditelusuri ke IV, DV, atau CV yang spesifik | Framework backend memetakan IV; collector metrik memetakan DV; DB dan environment memetakan CV. |
| Modularity | ✅ — framework, data layer, dan load generator dapat dipisah | Spring Boot dan .NET diperlakukan sebagai modul yang dapat diganti tanpa mengubah skenario beban. |
| Controllability | ✅ — CV dieksternalisasi sebagai parameter tetap | Dataset seed, index MongoDB, ukuran instance, dan load profile ditetapkan sebelum eksperimen. |
| Measurability | ✅ — DV diukur otomatis selama run | Load-testing dan monitoring menghasilkan RPS, p95 latency, CPU, memory, dan error rate secara terstruktur. |

**Prinsip mana yang paling sulit dipenuhi?** Controllability
**Strategi untuk mengatasinya:**
> Gunakan container/VM yang identik, pin versi runtime dan MongoDB, simpan seluruh parameter eksperimen di config file, lalu validasi environment sebelum setiap run.

---

## Latihan 3 — Ablation Study Planning

Jika sistem memiliki 3 komponen utama, rencanakan ablation study.

| Kondisi | Komponen A | Komponen B | Komponen C | Hasil yang Diharapkan |
|---------|-----------|-----------|-----------|----------------------|
| Full | ✅ Spring Boot | ✅ MongoDB CRUD layer | ✅ Monitoring + load-test pipeline | Baseline penuh untuk perbandingan |
| – A | ❌ ganti menjadi .NET | ✅ MongoDB CRUD layer | ✅ Monitoring + load-test pipeline | Mengisolasi pengaruh framework backend |
| – B | ✅ Spring Boot | ❌ perubahan pada skenario akses data | ✅ Monitoring + load-test pipeline | Menguji kontribusi akses data terhadap throughput dan latency |
| – C | ✅ Spring Boot | ✅ MongoDB CRUD layer | ❌ tanpa monitoring/aggregator metrik | Menunjukkan seberapa penting pipeline pengukuran bagi analisis |

**Komponen mana yang diprediksi paling berkontribusi?** Komponen framework backend dan data access layer
**Mengapa?**
> Karena perbedaan implementasi framework dan cara menangani request CRUD paling langsung memengaruhi throughput dan tail latency, sedangkan monitoring hanya memfasilitasi pengukuran.

---

## Refleksi

> Apa risiko jika sistem dibangun seperti produk (monolitik, fitur lengkap) lalu baru dilakukan eksperimen? Mengapa arsitektur modular penting untuk riset?

**Jawaban:**
> Jika sistem dibangun seperti produk monolitik, variabel akan saling bercampur sehingga penyebab perbedaan hasil sulit diidentifikasi. Arsitektur modular penting karena memungkinkan isolasi variabel, kontrol terhadap kondisi eksperimen, dan reprodusibilitas yang lebih baik.
> Dengan pemisahan komponen, peneliti bisa mengubah satu faktor pada satu waktu, memastikan CV tetap konstan, dan membaca output eksperimen sebagai bukti untuk RQ, bukan sebagai efek samping desain produk.
