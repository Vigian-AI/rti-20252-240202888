"""
import_data.py
Mengimpor IKEA_product_catalog.csv ke koleksi MongoDB.

Usage:
    python import_data.py \
        --source /data/IKEA_product_catalog.csv \
        --uri    mongodb://localhost:27017 \
        --db     benchmark_db \
        --collection ikea_products
"""

import argparse
import csv
import sys
import time
from pymongo import MongoClient, ASCENDING
from pymongo.errors import BulkWriteError


BATCH_SIZE = 5_000   # dokumen per batch insert


def parse_row(row: dict) -> dict:
    """Konversi tipe data dari string CSV ke tipe yang sesuai."""
    for float_field in ("product_rating", "product_rating_count", "price"):
        raw = row.get(float_field, "")
        try:
            row[float_field] = float(raw) if raw and raw.lower() != "none" else None
        except ValueError:
            row[float_field] = None
    return row


def main():
    parser = argparse.ArgumentParser(description="Import IKEA CSV ke MongoDB")
    parser.add_argument("--source",     required=True,  help="Path ke file CSV")
    parser.add_argument("--uri",        default="mongodb://localhost:27017")
    parser.add_argument("--db",         default="benchmark_db")
    parser.add_argument("--collection", default="ikea_products")
    parser.add_argument("--drop",       action="store_true",
                        help="Drop koleksi sebelum import (default: skip duplikat)")
    args = parser.parse_args()

    client = MongoClient(args.uri, serverSelectionTimeoutMS=10_000)
    try:
        client.admin.command("ping")
    except Exception as e:
        print(f"[ERROR] Tidak bisa terhubung ke MongoDB: {e}", file=sys.stderr)
        sys.exit(1)

    db   = client[args.db]
    col  = db[args.collection]

    if args.drop:
        col.drop()
        print("[INFO] Koleksi di-drop.")

    # Index pada unique_id untuk mempercepat query benchmark
    col.create_index([("unique_id", ASCENDING)], unique=True, background=True)

    print(f"[INFO] Membaca {args.source} ...")
    start = time.time()
    total_inserted = 0
    total_skipped  = 0
    batch: list[dict] = []

    with open(args.source, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            batch.append(parse_row(dict(row)))
            if len(batch) >= BATCH_SIZE:
                inserted, skipped = _insert_batch(col, batch)
                total_inserted += inserted
                total_skipped  += skipped
                batch = []
                print(f"  ... {total_inserted:,} inserted, {total_skipped:,} skipped", end="\r")

    if batch:
        inserted, skipped = _insert_batch(col, batch)
        total_inserted += inserted
        total_skipped  += skipped

    elapsed = time.time() - start
    print(f"\n[DONE] {total_inserted:,} dokumen diimpor, "
          f"{total_skipped:,} dilewati (duplikat) dalam {elapsed:.1f}s")


def _insert_batch(col, batch: list[dict]) -> tuple[int, int]:
    """Insert batch dengan ordered=False agar duplikat tidak menghentikan proses."""
    try:
        result = col.insert_many(batch, ordered=False)
        return len(result.inserted_ids), 0
    except BulkWriteError as bwe:
        inserted = bwe.details.get("nInserted", 0)
        skipped  = len(batch) - inserted
        return inserted, skipped


if __name__ == "__main__":
    main()
