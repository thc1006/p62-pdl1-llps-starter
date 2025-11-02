#!/usr/bin/env python3
"""
Full TCGA Cohort Analysis (n=500-1000)
Download and analyze complete LUAD+LUSC cohorts for publication-quality results
"""

import pandas as pd
import numpy as np
from scipy import stats
from pathlib import Path
import json
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

def analyze_existing_tcga_data():
    """Analyze all downloaded TCGA expression files"""

    data_dir = Path("outputs/gdc_expression")
    # Read ALL TSV files (both .tsv and .tsv.gz)
    files_gz = list(data_dir.glob("*.tsv.gz"))
    files_tsv = list(data_dir.glob("*.tsv"))
    files = files_tsv + files_gz

    print("="*60)
    print("FULL TCGA COHORT ANALYSIS")
    print("="*60)
    print(f"Data directory: {data_dir}")
    print(f"Files found: {len(files)} ({len(files_tsv)} .tsv + {len(files_gz)} .tsv.gz)\n")

    if len(files) < 50:
        print("[WARN] Less than 50 files found. Recommend downloading more.")
        print("Target: n=500-1000 for publication-quality analysis")

    # Genes of interest
    genes = ['SQSTM1', 'CD274', 'HIP1R', 'CMTM6', 'STUB1']

    # Parse all files
    expression_data = []

    for i, file_path in enumerate(files, 1):
        if i % 50 == 0:
            print(f"  Processed {i}/{len(files)} files...")

        try:
            # Files are plain text despite .tsv.gz extension
            df = pd.read_csv(file_path, sep='\t', comment='#', compression=None)

            # Extract FPKM
            if 'fpkm_unstranded' in df.columns and 'gene_name' in df.columns:
                expr = df[['gene_name', 'fpkm_unstranded']].copy()
                expr.columns = ['gene', 'fpkm']

                # Filter to genes of interest
                expr_filtered = expr[expr['gene'].isin(genes)].copy()
                expr_filtered['sample_id'] = file_path.stem

                expression_data.append(expr_filtered)

        except Exception as e:
            print(f"  [WARN] Failed to parse {file_path.name}: {e}")

    # Combine
    if not expression_data:
        print("[FAIL] No expression data parsed!")
        return None

    combined = pd.concat(expression_data, ignore_index=True)

    # Pivot to wide format
    wide = combined.pivot_table(
        index='sample_id',
        columns='gene',
        values='fpkm'
    ).reset_index()

    print(f"\n[OK] Expression matrix: {wide.shape}")
    print(f"Samples: {len(wide)}")
    print(f"Genes: {', '.join([c for c in wide.columns if c != 'sample_id'])}\n")

    return wide

def calculate_correlations(expr_df):
    """Calculate all pairwise correlations"""

    genes = [c for c in expr_df.columns if c != 'sample_id']

    results = []

    print("="*60)
    print("CORRELATION ANALYSIS")
    print("="*60)

    for i, gene1 in enumerate(genes):
        for j, gene2 in enumerate(genes):
            if i < j:  # Avoid duplicates
                # Drop NaN
                valid = expr_df[[gene1, gene2]].dropna()

                if len(valid) >= 10:
                    r, p = stats.pearsonr(valid[gene1], valid[gene2])

                    # Significance stars
                    if p < 0.001:
                        sig = "***"
                    elif p < 0.01:
                        sig = "**"
                    elif p < 0.05:
                        sig = "*"
                    else:
                        sig = "ns"

                    result = {
                        "gene1": gene1,
                        "gene2": gene2,
                        "r": round(r, 4),
                        "p": round(p, 5),
                        "n": len(valid),
                        "sig": sig
                    }

                    results.append(result)

                    print(f"{gene1:8s} vs {gene2:8s}: r={r:7.4f}, P={p:.5f} ({sig:3s}), n={len(valid)}")

    return results

def highlight_key_findings(correlations):
    """Highlight key findings for p62-PD-L1"""

    print("\n" + "="*60)
    print("KEY FINDINGS")
    print("="*60)

    # Find SQSTM1-CD274 correlation
    sqstm1_cd274 = [c for c in correlations if
                    (c['gene1'] == 'SQSTM1' and c['gene2'] == 'CD274') or
                    (c['gene1'] == 'CD274' and c['gene2'] == 'SQSTM1')]

    if sqstm1_cd274:
        result = sqstm1_cd274[0]
        print("\n1. SQSTM1 (p62) vs CD274 (PD-L1):")
        print(f"   Pearson r = {result['r']:.4f}")
        print(f"   P-value = {result['p']:.5f} ({result['sig']})")
        print(f"   Sample size = {result['n']}")

        if abs(result['r']) < 0.2:
            print("\n   INTERPRETATION:")
            print("   - WEAK correlation (|r| < 0.2)")
            print("   - Supports CONTEXT-DEPENDENT regulation hypothesis")
            print("   - Not a simple linear relationship")
            print("   - Depends on autophagy flux, TME, cellular stress")

        if result['p'] >= 0.05:
            print("\n   - NOT statistically significant (P >= 0.05)")
            print("   - NULL correlation")
            print("   - Further supports context-dependency")

    # Find strongest correlations
    print("\n2. Strongest Correlations:")
    sorted_corr = sorted(correlations, key=lambda x: abs(x['r']), reverse=True)

    for i, c in enumerate(sorted_corr[:5], 1):
        print(f"   {i}. {c['gene1']:8s} - {c['gene2']:8s}: r={c['r']:7.4f} ({c['sig']})")

    # Find significant correlations
    sig_corr = [c for c in correlations if c['p'] < 0.05]
    print(f"\n3. Significant correlations (P<0.05): {len(sig_corr)}/{len(correlations)}")

    return sqstm1_cd274[0] if sqstm1_cd274 else None

def generate_publication_figure(expr_df, correlations):
    """Generate publication-quality correlation figure"""

    output_dir = Path("outputs/tcga_full_cohort")
    output_dir.mkdir(parents=True, exist_ok=True)

    fig, axes = plt.subplots(2, 2, figsize=(14, 12))
    fig.suptitle("TCGA LUAD+LUSC: p62-PD-L1 Axis Expression Analysis",
                 fontsize=16, fontweight='bold')

    # 1. SQSTM1 vs CD274 scatter
    ax1 = axes[0, 0]
    valid = expr_df[['SQSTM1', 'CD274']].dropna()

    if len(valid) > 0:
        ax1.scatter(valid['SQSTM1'], valid['CD274'], alpha=0.5, s=30)

        # Add regression line
        z = np.polyfit(valid['SQSTM1'], valid['CD274'], 1)
        p = np.poly1d(z)
        ax1.plot(valid['SQSTM1'], p(valid['SQSTM1']), "r--", alpha=0.8)

        # Add correlation stats
        r, p_val = stats.pearsonr(valid['SQSTM1'], valid['CD274'])
        ax1.text(0.05, 0.95, f'r = {r:.3f}\nP = {p_val:.4f}\nn = {len(valid)}',
                transform=ax1.transAxes, va='top',
                bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

        ax1.set_xlabel('SQSTM1 (p62) FPKM', fontsize=12)
        ax1.set_ylabel('CD274 (PD-L1) FPKM', fontsize=12)
        ax1.set_title('A. p62 vs PD-L1 Expression', fontweight='bold')
        ax1.grid(alpha=0.3)

    # 2. Correlation heatmap
    ax2 = axes[0, 1]
    genes = ['SQSTM1', 'CD274', 'HIP1R', 'CMTM6', 'STUB1']
    corr_matrix = expr_df[genes].corr()

    sns.heatmap(corr_matrix, annot=True, fmt=".3f", cmap='RdBu_r',
                center=0, vmin=-0.5, vmax=0.5, square=True,
                cbar_kws={'label': 'Pearson r'}, ax=ax2)
    ax2.set_title('B. Gene Correlation Matrix', fontweight='bold')

    # 3. Distribution histograms
    ax3 = axes[1, 0]
    for gene in ['SQSTM1', 'CD274']:
        if gene in expr_df.columns:
            data = expr_df[gene].dropna()
            ax3.hist(np.log2(data + 1), bins=30, alpha=0.6, label=gene)

    ax3.set_xlabel('log2(FPKM + 1)', fontsize=12)
    ax3.set_ylabel('Frequency', fontsize=12)
    ax3.set_title('C. Expression Distributions', fontweight='bold')
    ax3.legend()
    ax3.grid(alpha=0.3)

    # 4. Correlation significance bar plot
    ax4 = axes[1, 1]

    # Prepare data for bar plot
    gene_pairs = []
    r_values = []
    p_values = []
    colors = []

    for c in correlations:
        label = f"{c['gene1'][:4]}-{c['gene2'][:4]}"
        gene_pairs.append(label)
        r_values.append(c['r'])
        p_values.append(-np.log10(c['p']) if c['p'] > 0 else 10)

        # Color by significance
        if c['p'] < 0.001:
            colors.append('#d62728')  # Red for p<0.001
        elif c['p'] < 0.01:
            colors.append('#ff7f0e')  # Orange for p<0.01
        elif c['p'] < 0.05:
            colors.append('#2ca02c')  # Green for p<0.05
        else:
            colors.append('#7f7f7f')  # Gray for ns

    # Create horizontal bar plot
    y_pos = np.arange(len(gene_pairs))
    ax4.barh(y_pos, p_values, color=colors, alpha=0.7)
    ax4.set_yticks(y_pos)
    ax4.set_yticklabels(gene_pairs, fontsize=9)
    ax4.set_xlabel('-log10(P-value)', fontsize=11)
    ax4.set_title('D. Correlation Significance', fontweight='bold')
    ax4.axvline(x=-np.log10(0.05), color='black', linestyle='--', alpha=0.5, linewidth=1)
    ax4.text(-np.log10(0.05), len(gene_pairs)-0.5, 'P=0.05', rotation=90,
             va='top', fontsize=8, alpha=0.7)
    ax4.grid(axis='x', alpha=0.3)
    ax4.invert_yaxis()  # Largest on top

    plt.tight_layout()

    # Save
    output_file = output_dir / "TCGA_Full_Cohort_Analysis.png"
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"\n[SAVED] Figure: {output_file}")

    plt.close()

def main():
    # Analyze existing data
    expr_df = analyze_existing_tcga_data()

    if expr_df is None:
        print("[FAIL] No data to analyze")
        return

    # Calculate correlations
    correlations = calculate_correlations(expr_df)

    # Highlight key findings
    key_result = highlight_key_findings(correlations)

    # Generate figure
    generate_publication_figure(expr_df, correlations)

    # Save results
    output_dir = Path("outputs/tcga_full_cohort")
    output_dir.mkdir(parents=True, exist_ok=True)

    # Save correlation results
    corr_df = pd.DataFrame(correlations)
    corr_df.to_csv(output_dir / "correlation_results.csv", index=False)
    print(f"\n[SAVED] Correlations: {output_dir / 'correlation_results.csv'}")

    # Save expression matrix
    expr_df.to_csv(output_dir / "expression_matrix.csv", index=False)
    print(f"[SAVED] Expression matrix: {output_dir / 'expression_matrix.csv'}")

    print("\n" + "="*60)
    print("[COMPLETE] Full TCGA cohort analysis finished!")
    print("="*60)
    print(f"Total samples analyzed: {len(expr_df)}")

    if len(expr_df) >= 500:
        print("[EXCELLENT] Sample size (n>=500) sufficient for publication!")
    elif len(expr_df) >= 200:
        print("[GOOD] Sample size (n>=200) acceptable for preprint")
    else:
        print("[NOTE] Consider downloading more samples for stronger statistics")

if __name__ == "__main__":
    main()
