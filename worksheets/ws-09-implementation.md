# WS-09: Implementation & Environment

> **Bab 9 — Implementasi Riset & Kontrol Lingkungan**

---

## Ringkasan Materi

### Implementasi Riset ≠ Coding Biasa

Tujuan implementasi riset bukan membuat software yang berfungsi, melainkan membangun **instrumen pengukuran yang konsisten**. Setiap modul harus di-mapping ke variabel (dari Bab 6), parameter harus config-driven, dan logging aktif dari hari pertama.

> **Mengapa reproducibility penting?** Sains dibangun di atas prinsip verifikasi — temuan harus bisa dikonfirmasi oleh peneliti lain. _Replicability crisis_ yang terjadi di banyak paper riset ML/AI disebabkan oleh environment tidak terdokumentasi: orang lain tidak bisa reproduksi, hasil diragukan, kepercayaan terhadap temuan hilang. Prinsip: **dokumentasi environment = snapshot kredibilitas riset Anda.**

### Reproducible Implementation Model

```
Design → Implementation → Environment Setup → Execution Consistency → Reproducibility → Trustworthy Result
```

Setiap transisi memiliki syarat:
- Design → Implementation: kode sesuai mapping variabel-ke-komponen
- Implementation → Environment: versi, dependency, seed, path, OS eksplisit
- Environment → Consistency: seed terkunci, urutan deterministik
- Consistency → Reproducibility: dokumentasi lengkap
- Reproducibility → Trust: siapa pun ikuti dokumentasi → hasil sama/serupa

### Repeatability vs Reproducibility

| Level | Peneliti | Environment | Hasil |
|-------|---------|-------------|-------|
| **Repeatability** | Sama | Sama | Sama persis |
| **Reproducibility** | Berbeda | Berbeda (ikuti docs) | Sama/serupa |

Capai **repeatability** dulu, baru **reproducibility**.

### Engineering vs Research Perspective

| Aspek | Engineering | Research |
|-------|-----------|---------|
| Tujuan | Sistem berfungsi untuk user | Instrumen pengukuran konsisten |
| Dependency | Update ke terbaru | Lock di versi spesifik |
| Testing | Unit, integration, E2E | Repeatability test (run ulang → sama?) |
| Dokumentasi | User guide, API docs | Environment spec, execution steps, expected output |
| Config | Default masuk akal | Setiap parameter eksplisit & adjustable |

### Jebakan Kognitif

1. Menunda environment setup → bug sulit dilacak
2. Tidak pakai version control → hasil tidak bisa direkonstruksi
3. Menolak Docker/container → "di laptop saya bisa" saat review
   - **Docker** = teknologi container yang "membungkus" aplikasi beserta seluruh dependency-nya dalam satu unit terisolasi. Hasilnya: kode berjalan identik di laptop, server, maupun reviewer lain. Intro singkat: `docker run -v $(pwd):/workspace environment-image python run_experiment.py`
4. 3× hasil sama ≠ repeatable (bisa cache/state tersimpan)

### Dependency Locking

Mengandalkan "install library terbaru" berbahaya: versi berbeda = perilaku berbeda = hasil tidak reproducible. Praktik:
- **Python**: buat `requirements.txt` dengan versi eksplisit: `scikit-learn==1.3.2`, lalu kunci dengan `pip freeze > requirements.txt`
- **Conda**: gunakan `conda env export > environment.yml` untuk snapshot lengkap
- **Node.js/R/Julia**: gunakan `package-lock.json` / `renv.lock` / `Project.toml` — semua fungsi serupa: lock versi + hash

### Istilah Penting

- **Environment Specification** — Deskripsi lengkap: hardware, OS, runtime, library + versi, config, seed
- **Dependency** — Komponen eksternal yang harus di-lock versinya
- **Config-driven** — Parameter dieksternalisasi ke file konfigurasi, bukan hardcode

---

## Template A.9 — Dokumentasi Setup Eksperimen

```
EXPERIMENT SETUP DOCUMENTATION

Hardware:
  CPU     : ____________________
  RAM     : ____________________
  GPU     : ____________________
  Storage : ____________________

Software:
  OS        : ____________________
  Runtime   : ____________________
  Framework : ____________________

Dependencies:
| Library | Version | Sumber | Hash/Checksum |
|---------|---------|--------|---------------|
|         |         |        |               |
|         |         |        |               |

Konfigurasi:
  Config file     : ____________________
  Random seed     : ____________________
  Hyperparameters : ____________________

Reproducibility Check:
  [ ] Dependency terdokumentasi (requirements.txt / lock file)
  [ ] Seed ditetapkan di semua level (Python, NumPy, framework)
  [ ] Config di version control
  [ ] README instruksi reproduksi lengkap
```

---

## Latihan 1 — Environment Specification

Dokumentasikan environment untuk eksperimen perbandingan Spring Boot vs .NET pada MongoDB.

**Host Machine (mesin fisik yang menjalankan Docker):**

| Komponen | Spesifikasi |
|----------|------------|
| CPU | AMD Ryzen 7 8845HS w/ Radeon 780M Graphics, 8 Core / 16 Thread |
| RAM | 16 GB |
| GPU | AMD Radeon 780M (integrated — tidak digunakan, eksperimen CPU-only) |
| Storage | WD PC SN5000S 512 GB NVMe SSD |
| OS | Windows 11 Home Single Language (Build 10.0.26200) |
| Docker | Docker Desktop 29.1.2 (engine berjalan di WSL2 backend) |

**Container Environment (semua service berjalan di Docker):**

| Komponen | Spesifikasi |
|----------|------------|
| Runtime Spring Boot | Eclipse Temurin JDK 21 LTS (`eclipse-temurin:21-jre-alpine`) |
| Runtime .NET | .NET 8 LTS (`mcr.microsoft.com/dotnet/aspnet:8.0-alpine`) |
| Database | MongoDB 7.0 (`mongo:7.0`) |
| Load Testing | k6 v0.51.0 (`grafana/k6:0.51.0`) |
| Orchestrasi | Docker Compose v2 (semua service didefinisikan di `docker-compose.yml`) |
| Random Seed | Dataset seed MongoDB: 42 (digunakan saat populate data awal via skrip) |

**Dependencies (per service — versi di-pin di Dockerfile / docker-compose.yml):**

| Library | Version | Konteks Service | Alasan Dibutuhkan |
|---------|---------|-----------------|-------------------|
| spring-boot-starter-web | 3.3.1 | springboot-api | REST endpoint dan embedded Tomcat |
| spring-boot-starter-data-mongodb | 3.3.1 | springboot-api | Driver dan repository MongoDB untuk Spring Boot |
| Microsoft.AspNetCore.App | 8.0.x | dotnet-api | Runtime ASP.NET Core minimal API |
| MongoDB.Driver | 2.25.0 | dotnet-api | Driver resmi MongoDB untuk .NET |
| k6 | 0.51.0 | k6 container | Load testing — menghasilkan RPS dan latency terukur |

---

## Latihan 2 — Repeatability Test Plan

Rancang tes repeatability untuk eksperimen perbandingan Spring Boot vs .NET.

| Run | Seed | Metrik Utama | Hasil Sama? |
|-----|------|-------------|-------------|
| 1 | 42 (dataset seed MongoDB) | Throughput (RPS) rata-rata steady-state & p95 latency (ms) | — (baseline) |
| 2 | 42 | Throughput (RPS) rata-rata steady-state & p95 latency (ms) | [ ] Ya / [ ] Tidak |
| 3 | 42 | Throughput (RPS) rata-rata steady-state & p95 latency (ms) | [ ] Ya / [ ] Tidak |

**Jika hasil berbeda, kemungkinan penyebab:**

> Penyebab umum non-repeatability:
> - **Thermal throttling** — CPU overheating pada run berturut-turut → clock speed turun → waktu eksekusi berubah
> - **Background process host** — antivirus scan, Windows Update, atau cloud sync aktif di host saat run berlangsung
> - **Cache dari run sebelumnya** — MongoDB WiredTiger cache atau koneksi pool belum di-reset antar-run
> - **Container state tersimpan** — container tidak di-recreate antar-run sehingga JVM sudah warm dari run sebelumnya

Untuk eksperimen ini, penyebab spesifik yang paling mungkin:
1. **JVM warm-up (JIT compilation)** — container Spring Boot pada run pertama belum teroptimasi JIT. Mitigasi: tambahkan warm-up period 30 detik sebelum window pengukuran, **dan recreate container** antar-run (`docker compose down && docker compose up`) agar JVM state bersih.
2. **MongoDB WiredTiger cache** — data dari run sebelumnya mungkin masih di cache sehingga run berikutnya lebih cepat. Mitigasi: restart container MongoDB antar-run atau jalankan `db.adminCommand({setParameter:1, wiredTigerEngineRuntimeConfig:"cache_size=0"})` untuk flush.
3. **WSL2 / Docker Desktop resource contention** — Docker Desktop di Windows menggunakan WSL2; proses host (OneDrive, Windows Defender) bisa mengkonsumsi CPU yang sama. Mitigasi: suspend real-time protection, tutup aplikasi background berat sebelum eksperimen.
4. **Ryzen 7 8845HS boost clock variability** — CPU ini memiliki rentang TDP yang lebar; performa bisa berbeda tergantung thermal headroom. Mitigasi: set Docker resource limit eksplisit (`cpus: "4"`, `memory: "4g"`) di `docker-compose.yml` agar beban terisolasi.

**Checklist kontrol yang sudah diterapkan:**
- [x] Random seed di-set di semua level (dataset seed MongoDB = 42, populate data deterministik via skrip)
- [x] Container di-recreate penuh antar-run (`docker compose down -v && docker compose up -d`) untuk reset JVM dan cache state
- [x] Resource limit container dikunci di `docker-compose.yml` (cpus, memory) agar tidak berubah antar-run
- [x] Config file yang sama untuk semua run (semua parameter eksperimen di `experiment-config.yaml`, di-mount ke container)

---

## Latihan 3 — README Eksperimen

Tulis README minimum untuk eksperimen perbandingan Spring Boot vs .NET pada MongoDB.

```
# Judul Eksperimen: Perbandingan Throughput dan p95 Latency REST API Spring Boot vs .NET pada MongoDB

## 1. Environment
  Host OS  : Windows 11 Home Single Language (Build 10.0.26200)
  Host CPU : AMD Ryzen 7 8845HS, 8C/16T
  Host RAM : 16 GB
  Storage  : WD PC SN5000S 512 GB NVMe SSD
  Docker   : Docker Desktop 29.1.2 (WSL2 backend)

  Container resource limits (dikunci di docker-compose.yml):
    springboot-api : cpus=2, memory=2g
    dotnet-api     : cpus=2, memory=2g
    mongodb        : cpus=2, memory=2g
    k6             : cpus=2, memory=1g

  Image versions:
    Spring Boot API : eclipse-temurin:21-jre-alpine  (JDK 21 LTS)
    .NET API        : mcr.microsoft.com/dotnet/aspnet:8.0-alpine (.NET 8 LTS)
    MongoDB         : mongo:7.0
    k6              : grafana/k6:0.51.0

## 2. Installation
  # Prasyarat: Docker Desktop 29.x terinstall dan berjalan
  git clone <repo-url>
  cd benchmark-experiment

  # Build semua image
  docker compose build

  # Populate dataset (seed = 42, 100.000 dokumen)
  docker compose run --rm data-seeder python populate_data.py --seed 42 --count 100000

## 3. Data
  Sumber  : Data sintetis yang digenerate via container data-seeder (Python 3.12)
  Format  : Dokumen JSON pada koleksi MongoDB (fields: _id, name, value, timestamp)
  Ukuran  : 100.000 dokumen (~50 MB)
  Seed    : 42 (deterministik, reproducible)
  Lokasi  : MongoDB volume di-mount ke ./data/mongodb/

## 4. Execution
  # Jalankan satu siklus eksperimen lengkap (3 run x 2 framework):
  docker compose run --rm experiment-runner python run_experiment.py \
    --config experiment-config.yaml \
    --runs 3

  # Atau jalankan manual per framework:
  # Spring Boot
  docker compose up -d mongodb springboot-api
  docker compose run --rm k6 run /scripts/load-test.js \
    -e TARGET=http://springboot-api:8080 --out json=/results/sb-run1.json

  # .NET
  docker compose up -d mongodb dotnet-api
  docker compose run --rm k6 run /scripts/load-test.js \
    -e TARGET=http://dotnet-api:5000 --out json=/results/dn-run1.json

  # Setelah setiap run, recreate container untuk reset state:
  docker compose down -v && docker compose up -d

## 5. Configuration
  File    : experiment-config.yaml (di-mount ke semua container)
  Parameter kunci:
    virtual_users  : 50
    ramp_up        : 30s        
    steady_state   : 120s
    ramp_down      : 10s
    warmup_duration: 30s   (tidak dihitung dalam pengukuran)
    db_seed        : 42
    mongo_uri      : mongodb://mongodb:27017/benchmark_db
    repeat_runs    : 3
    container_cpu  : "2"
    container_mem  : "2g"

## 6. Expected Output
  Lokasi  : ./results/ (di-mount dari container)
  Format  : JSON per run, CSV agregat setelah analisis

  Contoh output per run (JSON):
    {
      "framework": "spring-boot",
      "run": 1,
      "throughput_rps": 1250.4,
      "p95_latency_ms": 48.7,
      "p99_latency_ms": 72.1,
      "error_rate_pct": 0.0,
      "docker_image": "eclipse-temurin:21-jre-alpine",
      "mongo_image": "mongo:7.0",
      "config": "experiment-config.yaml",
      "timestamp": "2026-06-22T10:00:00Z"
    }

  Setelah semua run selesai, jalankan analisis:
    docker compose run --rm analyzer python analyze.py \
      --input /results/ --output /results/summary.csv
  untuk mendapatkan rata-rata, std dev, dan hasil uji statistik
  (Shapiro-Wilk -> t-test atau Mann-Whitney U, alpha=0.05, effect size Cohen's d).
```

---

## Refleksi

> Apakah eksperimen ini bisa direproduksi oleh orang lain tanpa bantuan Anda? Komponen apa yang masih hilang?

**Level saat ini:** [x] Repeatability / [ ] Reproducibility / [ ] Belum keduanya

> Repeatability sudah dirancang dengan kuat: seed deterministik, resource limit container dikunci, `docker compose down -v` antar-run untuk reset state penuh, dan semua parameter di `experiment-config.yaml`. Dengan Docker, reproducibility lintas OS juga jauh lebih dekat karena environment dibungkus dalam image — reviewer di Linux atau macOS bisa menjalankan setup yang sama. Namun beberapa komponen masih dalam tahap rencana.

**Komponen yang belum terdokumentasi:**
> 1. **Dockerfile dan docker-compose.yml belum ditulis** — image versions sudah ditentukan di README, tapi file konfigurasi aktual (Dockerfile untuk springboot-api dan dotnet-api, docker-compose.yml lengkap dengan resource limits) belum ada di repo. Ini komponen paling kritis.
> 2. **Skrip eksperimen belum diimplementasi** — `populate_data.py`, `run_experiment.py`, `load-test.js` (k6 script), dan `analyze.py` masih berupa placeholder di README. Harus ditulis dan diuji sebelum eksekusi.
> 3. **Resource limit WSL2 belum dikonfigurasi** — Docker Desktop di Windows menggunakan WSL2; tanpa file `.wslconfig` yang membatasi CPU dan RAM untuk WSL2, host bisa mengalami resource contention dengan proses Windows lainnya. Perlu ditambahkan ke dokumentasi setup.
> 4. **Verifikasi image digest** — untuk reproducibility jangka panjang, image harus di-pin ke digest (`mongo@sha256:...`) bukan hanya tag, karena tag bisa di-update oleh maintainer tanpa notifikasi.
