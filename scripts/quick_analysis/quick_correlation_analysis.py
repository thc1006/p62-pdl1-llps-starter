#!/usr/bin/env python3
"""
Quick correlation analysis for SQSTM1-CD274 and visualization
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from pathlib import Path
import argparse

def calculate_correlations(df, gene1='SQSTM1', gene2='CD274'):
    """Calculate Pearson and Spearman correlations"""
    # Remove NaN values
    valid = df[[gene1, gene2]].dropna()

    if len(valid) < 10:
        print(f"Warning: Only {len(valid)} valid samples for correlation")
        return None

    # Pearson
    pearson_r, pearson_p = stats.pearsonr(valid[gene1], valid[gene2])

    # Spearman
    spearman_r, spearman_p = stats.spearmanr(valid[gene1], valid[gene2])

    results = {
        'n_samples': len(valid),
        'pearson_r': pearson_r,
        'pearson_p': pearson_p,
        'spearman_r': spearman_r,
        'spearman_p': spearman_p
    }

    return results, valid

def plot_correlation(valid_data, gene1, gene2, results, output_path, title=""):
    """Create correlation scatter plot"""
    fig, ax = plt.subplots(figsize=(8, 6))

    # Scatter plot
    ax.scatter(valid_data[gene1], valid_data[gene2], alpha=0.5, s=30)

    # Add regression line
    z = np.polyfit(valid_data[gene1], valid_data[gene2], 1)
    p = np.poly1d(z)
    x_line = np.linspace(valid_data[gene1].min(), valid_data[gene1].max(), 100)
    ax.plot(x_line, p(x_line), "r--", alpha=0.8, linewidth=2)

    # Labels
    ax.set_xlabel(f'{gene1} Expression (FPKM/TPM)', fontsize=12)
    ax.set_ylabel(f'{gene2} Expression (FPKM/TPM)', fontsize=12)

    # Title with stats
    stats_text = f"Pearson r={results['pearson_r']:.3f}, P={results['pearson_p']:.2e}\n"
    stats_text += f"Spearman ρ={results['spearman_r']:.3f}, P={results['spearman_p']:.2e}\n"
    stats_text += f"n={results['n_samples']}"

    ax.set_title(f"{title}\n{stats_text}", fontsize=10)

    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()

    print(f"  Saved plot: {output_path}")

def main():
    parser = argparse.ArgumentParser(description="Quick correlation analysis")
    parser.add_argument("--input", required=True, help="Expression matrix CSV")
    parser.add_argument("--gene1", default="SQSTM1", help="First gene (default: SQSTM1)")
    parser.add_argument("--gene2", default="CD274", help="Second gene (default: CD274)")
    parser.add_argument("--out", default="outputs/quick_analysis", help="Output directory")
    args = parser.parse_args()

    output_dir = Path(args.out)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Load data
    print(f"[Analysis] Loading data from {args.input}")
    df = pd.read_csv(args.input)
    print(f"[Analysis] Loaded {len(df)} samples")
    print(f"[Analysis] Columns: {df.columns.tolist()}")

    # Check if genes are present
    if args.gene1 not in df.columns or args.gene2 not in df.columns:
        print(f"ERROR: Genes {args.gene1} and/or {args.gene2} not found in data!")
        print(f"Available genes: {[c for c in df.columns if c not in ['case_id', 'project']]}")
        return

    # Overall correlation
    print(f"\n[Analysis] Overall {args.gene1}-{args.gene2} correlation:")
    overall_results, overall_valid = calculate_correlations(df, args.gene1, args.gene2)

    if overall_results:
        print(f"  Pearson r = {overall_results['pearson_r']:.3f}, P = {overall_results['pearson_p']:.2e}")
        print(f"  Spearman ρ = {overall_results['spearman_r']:.3f}, P = {overall_results['spearman_p']:.2e}")
        print(f"  n = {overall_results['n_samples']}")

        # Plot
        plot_correlation(
            overall_valid, args.gene1, args.gene2, overall_results,
            output_dir / f"{args.gene1}_{args.gene2}_overall_correlation.png",
            title=f"{args.gene1} vs {args.gene2} (All Samples)"
        )

        # Save results
        results_df = pd.DataFrame([overall_results])
        results_df['cohort'] = 'Overall'
        results_df.to_csv(output_dir / "correlation_results.csv", index=False)

    # Per-project correlation
    if 'project' in df.columns:
        print(f"\n[Analysis] Per-project correlations:")
        project_results = []

        for project in df['project'].unique():
            print(f"\n  Project: {project}")
            project_df = df[df['project'] == project]

            results, valid = calculate_correlations(project_df, args.gene1, args.gene2)

            if results:
                print(f"    Pearson r = {results['pearson_r']:.3f}, P = {results['pearson_p']:.2e}")
                print(f"    Spearman ρ = {results['spearman_r']:.3f}, P = {results['spearman_p']:.2e}")
                print(f"    n = {results['n_samples']}")

                # Plot
                plot_correlation(
                    valid, args.gene1, args.gene2, results,
                    output_dir / f"{args.gene1}_{args.gene2}_{project}_correlation.png",
                    title=f"{args.gene1} vs {args.gene2} ({project})"
                )

                results['cohort'] = project
                project_results.append(results)

        # Save all results
        if project_results:
            all_results = pd.DataFrame(project_results)
            all_results.to_csv(output_dir / "correlation_results_by_project.csv", index=False)

    # Summary
    print(f"\n[Analysis] ====== SUMMARY ======")
    print(f"Overall correlation: r={overall_results['pearson_r']:.3f}, P={overall_results['pearson_p']:.2e}")

    if overall_results['pearson_p'] < 0.01 and abs(overall_results['pearson_r']) > 0.3:
        print(f"\n✅ STRONG EVIDENCE: Significant positive correlation!")
        print(f"   → Proceed with deep mechanistic analysis (SaProt, FoldX, etc.)")
    elif overall_results['pearson_p'] < 0.05 and abs(overall_results['pearson_r']) > 0.2:
        print(f"\n⚠️  MODERATE EVIDENCE: Weak but significant correlation")
        print(f"   → Consider focusing on methodological framework + literature")
    else:
        print(f"\n❌ WEAK EVIDENCE: Correlation not significant or very weak")
        print(f"   → Pivot to methodological contribution only")

    print(f"\nResults saved to: {output_dir}")

if __name__ == "__main__":
    main()
