# Arsitektur Sistem dan Skema Database (Tahap 1)

Dokumen ini memuat diagram arsitektur komponen, alur resolusi kunci (mitigasi JWKS flooding), mekanisme ketahanan (fail-closed/fail-open), skema database PostgreSQL, dan skema cache Redis.

---

## 1. Arsitektur Komponen

Arsitektur sistem menggunakan pola hybrid caching dengan memisahkan Redis sebagai L1 cache (murni cache JWKS) dan PostgreSQL sebagai L2 source of truth serta rate limiter permanen.

```mermaid
graph TD
    Client[Client / Attacker] -->|Request dengan JWT| Gateway[API Gateway - Go/Echo]
    Gateway -->|L1 Cache Lookup <br> positive/negative| Redis[(Redis JWKS Cache)]
    Gateway -->|L2 Source of Truth & <br> Rate Limit Counter| Postgres[(PostgreSQL DB)]
```

---

## 2. Alur Resolusi Kunci (Mitigasi JWKS Flooding)

Mitigasi JWKS flooding meminimalkan beban query ke database melalui negative cache di Redis dan rate limiting atomik berbasis IP di PostgreSQL.

```mermaid
flowchart TD
    Start([Request masuk]) --> Parse[Gateway parsing header JWT & ambil kid]
    Parse --> CheckL1Pos{Cek Redis positive cache<br>jwks:kid:kid}
    CheckL1Pos -->|HIT| Verify[Verifikasi signature JWT]
    CheckL1Pos -->|MISS| CheckL1Neg{Cek Redis negative cache<br>jwks:negative:kid}
    CheckL1Neg -->|HIT| Reject401([Tolak Langsung - 401 Unauthorized])
    CheckL1Neg -->|MISS| CheckRL{UPSERT & cek rate_limit_counters<br>di PostgreSQL}
    CheckRL -->|EXCEEDED| SetNegCache[Set Redis negative cache<br>TTL ~60s]
    SetNegCache --> Reject429([Tolak - 429 Too Many Requests])
    CheckRL -->|OK| QueryDB{Query PostgreSQL<br>signing_keys WHERE kid = ? AND is_active}
    QueryDB -->|FOUND| SetPosCache[Set Redis positive cache<br>TTL ~300s]
    SetPosCache --> Verify
    QueryDB -->|NOT FOUND| SetNegCache2[Set Redis negative cache<br>TTL ~60s]
    SetNegCache2 --> Reject401
    Verify -->|Valid| Allow([Loloskan Request])
    Verify -->|Invalid| Reject401_2([Tolak - 401 Unauthorized])
```

---

## 3. Mekanisme Fail-Closed / Failover

Gateway dirancang dengan prinsip **fail-closed** untuk menjamin keamanan sistem apabila dependensi database atau cache mengalami gangguan.

```mermaid
flowchart TD
    Start([Koneksi Database/Redis Bermasalah]) --> CekRedis{Redis Down?}
    CekRedis -->|Ya| BypassRedis[Bypass Redis, lanjut langsung ke PostgreSQL]
    BypassRedis --> CekPostgres{PostgreSQL Down?}
    CekRedis -->|Tidak| CekPostgres
    CekPostgres -->|Ya| FailClosed[Fail-Closed: Tolak Request dengan HTTP 500 / 401]
    CekPostgres -->|Tidak| ProcessRequest[Proses rate-limit & verifikasi kunci via PostgreSQL]
```

---

## 4. Entity-Relationship Diagram (PostgreSQL)

Skema database PostgreSQL memisahkan tabel kunci penandatangan (`signing_keys`) dan tabel pencatat batas laju request (`rate_limit_counters`).

```mermaid
erDiagram
    signing_keys {
        varchar kid PK
        varchar kty
        varchar alg
        varchar use_type
        text n
        text e
        boolean is_active
        timestamptz created_at
        timestamptz expires_at
        timestamptz revoked_at
    }
    rate_limit_counters {
        inet client_ip PK
        timestamptz window_start PK
        integer request_count
        integer blocked_count
    }
```

---

## 5. Skema Cache Redis (L1 Cache JWKS)

Redis murni difungsikan sebagai L1 cache data JWKS dengan skema kunci sebagai berikut:

| Key Pattern | Tipe Data | TTL | Tujuan |
|---|---|---|---|
| `jwks:kid:<kid>` | STRING (JSON JWK) | ~300s | Cache positif untuk kunci signing yang valid |
| `jwks:negative:<kid>` | STRING (`"1"`) | ~60s | Cache negatif untuk `kid` yang tidak terdaftar di DB (mencegah database lookup berulang) |
