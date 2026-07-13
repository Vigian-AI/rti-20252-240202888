"""
analyze_results.py
Melakukan analisis statistik (normalitas Shapiro-Wilk, uji beda t-test/Mann-Whitney U,
dan effect size Cohen's d) serta menyimpan summary_stats.csv.
"""

import os
import pandas as pd
from scipy import stats
import numpy as np

def cohens_d(a, b):
    pooled_std = ((a.std(ddof=1)**2 + b.std(ddof=1)**2) / 2) ** 0.5
    if pooled_std == 0:
        return 0.0
    return (a.mean() - b.mean()) / pooled_std

def main():
    csv_path = "results/all_runs.csv"
    if not os.path.exists(csv_path):
        print(f"[ERROR] File {csv_path} tidak ditemukan. Silakan jalankan ekstraksi metrik terlebih dahulu.")
        return

    df = pd.read_csv(csv_path)
    sb = df[df["scenario"] == "spring-boot"]
    dn = df[df["scenario"] == "dotnet"]

    print("==================================================")
    print("           ANALISIS STATISTIK HASIL              ")
    print("==================================================")

    # 1. Shapiro-Wilk Normality Test
    print("\n1. Uji Normalitas (Shapiro-Wilk)")
    metrics = ["throughput_rps", "p95_latency_ms"]
    normality = {}
    
    for metric in metrics:
        _, p_sb = stats.shapiro(sb[metric])
        _, p_dn = stats.shapiro(dn[metric])
        sb_normal = p_sb > 0.05
        dn_normal = p_dn > 0.05
        normality[metric] = sb_normal and dn_normal
        
        print(f"  {metric}:")
        print(f"    - Spring Boot p = {p_sb:.4f} ({'Normal' if sb_normal else 'Tidak Normal'})")
        print(f"    - .NET        p = {p_dn:.4f} ({'Normal' if dn_normal else 'Tidak Normal'})")

    # 2. Hypothesis Testing & Effect Size
    print("\n2. Uji Signifikansi & Effect Size")
    for metric in metrics:
        is_normal = normality[metric]
        print(f"  {metric}:")
        if is_normal:
            t_stat, p_val = stats.ttest_ind(sb[metric], dn[metric])
            test_name = "t-test (Independent)"
        else:
            u_stat, p_val = stats.mannwhitneyu(sb[metric], dn[metric], alternative="two-sided")
            test_name = "Mann-Whitney U"
            
        d = cohens_d(sb[metric], dn[metric])
        
        print(f"    - Metode: {test_name}")
        print(f"    - p-value: {p_val:.4f}")
        print(f"    - Signifikan (a=0.05): {'Ya' if p_val < 0.05 else 'Tidak'}")
        print(f"    - Cohen's d: {d:.4f}")

    # 3. Summary Stats Table
    print("\n3. Ringkasan Deskriptif (Mean, SD, Min, Max)")
    summary = df.groupby("scenario")[["throughput_rps", "p95_latency_ms", "p99_latency_ms"]].agg(
        ["mean", "std", "min", "max"]
    )
    print(summary.round(2).to_string())
    
    summary.to_csv("results/summary_stats.csv")
    print("\n[DONE] Hasil ringkasan statistik ditulis ke results/summary_stats.csv")
    print("==================================================")

if __name__ == "__main__":
    main()
