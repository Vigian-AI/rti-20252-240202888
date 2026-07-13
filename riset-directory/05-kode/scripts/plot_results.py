import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def main():
    csv_path = "results/all_runs.csv"
    if not os.path.exists(csv_path):
        print(f"[ERROR] File {csv_path} tidak ditemukan.")
        return

    # Load data
    df = pd.read_csv(csv_path)
    sb = df[df["scenario"] == "spring-boot"]
    dn = df[df["scenario"] == "dotnet"]

    # Calculate means and standard deviations
    sb_throughput_mean = sb["throughput_rps"].mean()
    sb_throughput_std = sb["throughput_rps"].std()
    dn_throughput_mean = dn["throughput_rps"].mean()
    dn_throughput_std = dn["throughput_rps"].std()

    sb_p95_mean = sb["p95_latency_ms"].mean()
    sb_p95_std = sb["p95_latency_ms"].std()
    dn_p95_mean = dn["p95_latency_ms"].mean()
    dn_p95_std = dn["p95_latency_ms"].std()

    # Style configuration
    plt.rcParams['font.sans-serif'] = 'Arial'
    plt.rcParams['font.family'] = 'sans-serif'
    
    # Sleek colors
    colors = ['#FF6B6B', '#4D96FF']  # Coral Red for Spring Boot, Blue for .NET
    
    # ── GRAPH 1: Throughput (RPS) ──────────────────────────────────────────────
    fig, ax = plt.subplots(figsize=(6, 5), dpi=300)
    
    categories = ['Spring Boot', '.NET']
    means = [sb_throughput_mean, dn_throughput_mean]
    stds = [sb_throughput_std, dn_throughput_std]
    
    bars = ax.bar(categories, means, yerr=stds, color=colors, capsize=8, width=0.5, 
                  edgecolor='black', linewidth=0.8, alpha=0.9)
    
    # Grid and styling
    ax.set_ylabel('Throughput (Requests per Second)', fontsize=11, fontweight='bold')
    ax.set_title('Throughput Comparison (Mean \u00b1 SD)', fontsize=12, fontweight='bold', pad=15)
    ax.grid(axis='y', linestyle='--', alpha=0.5)
    ax.set_axisbelow(True)
    
    # Add values on top of bars
    for bar in bars:
        height = bar.get_height()
        ax.annotate(f'{height:.2f} RPS',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 5),  # 5 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom', fontsize=10, fontweight='bold')
                    
    # Clean spines
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    plt.tight_layout()
    plt.savefig('results/throughput_comparison.png', dpi=300)
    plt.close()
    print("[DONE] Throughput chart saved to results/throughput_comparison.png")

    # ── GRAPH 2: Latency p95 (ms) Log-Scale ─────────────────────────────────────
    fig, ax = plt.subplots(figsize=(6, 5), dpi=300)
    
    latency_means = [sb_p95_mean, dn_p95_mean]
    latency_stds = [sb_p95_std, dn_p95_std]
    
    bars = ax.bar(categories, latency_means, yerr=latency_stds, color=colors, capsize=8, width=0.5,
                  edgecolor='black', linewidth=0.8, alpha=0.9)
    
    # Grid and styling
    ax.set_ylabel('p95 Latency (Milliseconds) - Log Scale', fontsize=11, fontweight='bold')
    ax.set_yscale('log')  # Use log scale since difference is huge (2218ms vs 4.6ms)
    ax.set_title('p95 Latency Comparison (Log Scale, Mean \u00b1 SD)', fontsize=12, fontweight='bold', pad=15)
    ax.grid(axis='y', which='both', linestyle='--', alpha=0.5)
    ax.set_axisbelow(True)
    
    # Add values on top of bars
    for bar in bars:
        height = bar.get_height()
        ax.annotate(f'{height:.2f} ms',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 5),
                    textcoords="offset points",
                    ha='center', va='bottom', fontsize=10, fontweight='bold')
                    
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    plt.tight_layout()
    plt.savefig('results/latency_comparison.png', dpi=300)
    plt.close()
    print("[DONE] Latency chart saved to results/latency_comparison.png")

if __name__ == "__main__":
    main()
