"""
extract_metrics.py
Ekstrak metrik agregat dari output CSV k6 dan gabungkan ke all_runs.csv.

Usage:
    python extract_metrics.py --input results/ --output results/all_runs.csv
"""

import argparse
import csv
import os
import numpy as np
from pathlib import Path


def extract(filepath: Path) -> dict:
    """Baca satu file CSV k6 dan hitung metrik agregat."""
    filename = filepath.stem          # misal: sb-run-001
    scenario = "spring-boot" if filename.startswith("sb") else "dotnet"
    run_num  = filename.split("-")[-1]  # 001, 002, dst

    durations = []   # http_req_duration dalam ms (window steady-state)
    errors    = 0
    total     = 0

    with open(filepath, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            metric = row.get("metric_name", "")
            if metric == "http_req_duration":
                try:
                    durations.append(float(row["metric_value"]))
                    total += 1
                except ValueError:
                    pass
            elif metric == "http_req_failed":
                try:
                    errors += float(row["metric_value"])
                except ValueError:
                    pass

    if not durations:
        return {}

    arr = np.array(durations)
    # RPS: total request / durasi steady-state (120 detik)
    rps = round(total / 120, 2)

    return {
        "run_id":           filename,
        "scenario":         scenario,
        "throughput_rps":   rps,
        "p95_latency_ms":   round(float(np.percentile(arr, 95)), 2),
        "p99_latency_ms":   round(float(np.percentile(arr, 99)), 2),
        "mean_latency_ms":  round(float(np.mean(arr)), 2),
        "error_rate_pct":   round((errors / total) * 100, 4) if total > 0 else 0.0,
        "iterations_total": total,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input",  required=True, help="Folder berisi file CSV k6")
    parser.add_argument("--output", required=True, help="Path output all_runs.csv")
    args = parser.parse_args()

    results_dir = Path(args.input)
    csv_files   = sorted(results_dir.glob("*.csv"))

    rows = []
    for f in csv_files:
        if f.name == "all_runs.csv":
            continue
        print(f"  Memproses {f.name} ...")
        row = extract(f)
        if row:
            rows.append(row)

    if not rows:
        print("[ERROR] Tidak ada data ditemukan.")
        return

    fieldnames = list(rows[0].keys())
    with open(args.output, "w", newline="", encoding="utf-8") as out:
        writer = csv.DictWriter(out, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"\n[DONE] {len(rows)} run ditulis ke {args.output}")


if __name__ == "__main__":
    main()
