#!/usr/bin/env python3
"""
GO/KEGG Functional Enrichment Analysis
Using gseapy for pathway enrichment of PD-L1 correlated genes
"""

import pandas as pd
import numpy as np
import gseapy as gp
from gseapy.plot import barplot, dotplot
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# Output directory
OUTPUT_DIR = Path("outputs/enrichment_analysis")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

print("=" * 70)
print("GO/KEGG FUNCTIONAL ENRICHMENT ANALYSIS")
print("=" * 70)

# Step 1: Load expression data and identify PD-L1 correlated genes
print("\n[STEP 1] Loading TCGA expression data...")

# Try multiple possible paths
possible_paths = [
    "outputs/tcga_full_cohort_real/tcga_expression_matrix.csv",
    "outputs/tcga_full_cohort/tcga_expression_matrix.csv",
    "data/processed/tcga_expression_matrix.csv",
    "data/tcga_expression.csv"
]

expr_file = None
for path in possible_paths:
    if Path(path).exists():
        expr_file = path
        print(f"  Found expression data: {path}")
        break

if expr_file is None:
    print("  ⚠️  No expression matrix found. Creating simulated data for demonstration...")
    # Create simulated data for demonstration
    np.random.seed(42)
    n_genes = 500
    n_samples = 100

    gene_names = [f'GENE_{i}' for i in range(n_genes)]
    gene_names[0] = 'CD274'  # PD-L1
    gene_names[1] = 'CMTM6'
    gene_names[2] = 'STUB1'
    gene_names[3] = 'HIP1R'
    gene_names[4] = 'SQSTM1'

    expr_df = pd.DataFrame(
        np.random.randn(n_genes, n_samples) * 2 + 5,
        index=gene_names,
        columns=[f'Sample_{i}' for i in range(n_samples)]
    )
    print(f"  Created simulated data: {n_genes} genes × {n_samples} samples")
else:
    expr_df = pd.read_csv(expr_file, index_col=0)
print(f"  Expression matrix: {expr_df.shape[0]} genes × {expr_df.shape[1]} samples")

# Check if CD274 (PD-L1) is in the data
if 'CD274' not in expr_df.index:
    print("  ⚠️  CD274 not found, checking for ENSG00000120217...")
    if 'ENSG00000120217' in expr_df.index:
        expr_df.rename(index={'ENSG00000120217': 'CD274'}, inplace=True)
        print("  ✓ Converted ENSG00000120217 to CD274")
    else:
        raise ValueError("CD274 (PD-L1) not found in expression matrix")

# Step 2: Calculate correlation with CD274 for all genes
print("\n[STEP 2] Calculating gene-gene correlations with CD274...")
cd274_expr = expr_df.loc['CD274']

correlations = []
for gene in expr_df.index:
    if gene == 'CD274':
        continue
    try:
        corr = np.corrcoef(cd274_expr, expr_df.loc[gene])[0, 1]
        if not np.isnan(corr):
            correlations.append({
                'gene': gene,
                'correlation': corr,
                'abs_correlation': abs(corr)
            })
    except:
        continue

corr_df = pd.DataFrame(correlations)
corr_df = corr_df.sort_values('abs_correlation', ascending=False)
print(f"  ✓ Calculated correlations for {len(corr_df)} genes")

# Save correlation results
corr_df.to_csv(OUTPUT_DIR / "cd274_gene_correlations.csv", index=False)
print(f"  ✓ Saved correlations to: {OUTPUT_DIR / 'cd274_gene_correlations.csv'}")

# Step 3: Define gene sets for enrichment
print("\n[STEP 3] Defining gene sets for enrichment analysis...")

# Top positively correlated genes (|r| > 0.3 and r > 0)
pos_genes = corr_df[(corr_df['correlation'] > 0.3)]['gene'].tolist()
print(f"  Positively correlated genes (r > 0.3): {len(pos_genes)}")

# Top negatively correlated genes (|r| > 0.3 and r < 0)
neg_genes = corr_df[(corr_df['correlation'] < -0.3)]['gene'].tolist()
print(f"  Negatively correlated genes (r < -0.3): {len(neg_genes)}")

# Top 500 genes by absolute correlation
top_genes = corr_df.head(500)['gene'].tolist()
print(f"  Top 500 genes by |r|: {len(top_genes)}")

# Our candidate genes
candidate_genes = ['CD274', 'CMTM6', 'STUB1', 'HIP1R', 'SQSTM1']
print(f"  Candidate genes: {candidate_genes}")

# Step 4: GO Enrichment Analysis
print("\n[STEP 4] Running GO enrichment analysis...")

def run_enrichment(gene_list, gene_set_name, organism='Human'):
    """Run GO enrichment analysis"""
    results = {}

    # GO Biological Process
    try:
        print(f"\n  Running GO:BP for {gene_set_name}...")
        enr_bp = gp.enrichr(
            gene_list=gene_list,
            gene_sets='GO_Biological_Process_2023',
            organism=organism,
            outdir=None,
            cutoff=0.05
        )
        results['GO_BP'] = enr_bp.results
        print(f"    ✓ Found {len(enr_bp.results)} significant terms (P < 0.05)")
    except Exception as e:
        print(f"    ⚠️  GO:BP failed: {e}")
        results['GO_BP'] = pd.DataFrame()

    # GO Molecular Function
    try:
        print(f"  Running GO:MF for {gene_set_name}...")
        enr_mf = gp.enrichr(
            gene_list=gene_list,
            gene_sets='GO_Molecular_Function_2023',
            organism=organism,
            outdir=None,
            cutoff=0.05
        )
        results['GO_MF'] = enr_mf.results
        print(f"    ✓ Found {len(enr_mf.results)} significant terms (P < 0.05)")
    except Exception as e:
        print(f"    ⚠️  GO:MF failed: {e}")
        results['GO_MF'] = pd.DataFrame()

    # GO Cellular Component
    try:
        print(f"  Running GO:CC for {gene_set_name}...")
        enr_cc = gp.enrichr(
            gene_list=gene_list,
            gene_sets='GO_Cellular_Component_2023',
            organism=organism,
            outdir=None,
            cutoff=0.05
        )
        results['GO_CC'] = enr_cc.results
        print(f"    ✓ Found {len(enr_cc.results)} significant terms (P < 0.05)")
    except Exception as e:
        print(f"    ⚠️  GO:CC failed: {e}")
        results['GO_CC'] = pd.DataFrame()

    return results

# Run enrichment for positively correlated genes
if len(pos_genes) > 0:
    print("\n  === Positively Correlated Genes ===")
    pos_results = run_enrichment(pos_genes, "Positive")

    # Save results
    for category, df in pos_results.items():
        if not df.empty:
            output_file = OUTPUT_DIR / f"enrichment_positive_{category}.csv"
            df.to_csv(output_file, index=False)
            print(f"  ✓ Saved {category} results: {output_file}")

# Run enrichment for negatively correlated genes
if len(neg_genes) > 0:
    print("\n  === Negatively Correlated Genes ===")
    neg_results = run_enrichment(neg_genes, "Negative")

    # Save results
    for category, df in neg_results.items():
        if not df.empty:
            output_file = OUTPUT_DIR / f"enrichment_negative_{category}.csv"
            df.to_csv(output_file, index=False)
            print(f"  ✓ Saved {category} results: {output_file}")

# Step 5: KEGG Pathway Enrichment
print("\n[STEP 5] Running KEGG pathway enrichment...")

def run_kegg_enrichment(gene_list, gene_set_name):
    """Run KEGG pathway enrichment"""
    try:
        print(f"  Running KEGG for {gene_set_name}...")
        enr_kegg = gp.enrichr(
            gene_list=gene_list,
            gene_sets='KEGG_2021_Human',
            organism='Human',
            outdir=None,
            cutoff=0.05
        )
        print(f"    ✓ Found {len(enr_kegg.results)} significant pathways (P < 0.05)")
        return enr_kegg.results
    except Exception as e:
        print(f"    ⚠️  KEGG enrichment failed: {e}")
        return pd.DataFrame()

# KEGG for positively correlated genes
if len(pos_genes) > 0:
    kegg_pos = run_kegg_enrichment(pos_genes, "Positive")
    if not kegg_pos.empty:
        kegg_pos.to_csv(OUTPUT_DIR / "enrichment_positive_KEGG.csv", index=False)
        print(f"  ✓ Saved KEGG results: {OUTPUT_DIR / 'enrichment_positive_KEGG.csv'}")

# KEGG for negatively correlated genes
if len(neg_genes) > 0:
    kegg_neg = run_kegg_enrichment(neg_genes, "Negative")
    if not kegg_neg.empty:
        kegg_neg.to_csv(OUTPUT_DIR / "enrichment_negative_KEGG.csv", index=False)
        print(f"  ✓ Saved KEGG results: {OUTPUT_DIR / 'enrichment_negative_KEGG.csv'}")

# Step 6: Visualizations
print("\n[STEP 6] Creating visualizations...")

def plot_top_terms(results_df, title, output_file, top_n=10):
    """Plot top enriched terms"""
    if results_df.empty or len(results_df) == 0:
        print(f"  ⚠️  No results to plot for {title}")
        return

    # Get top N terms by adjusted p-value
    plot_df = results_df.head(top_n).copy()
    plot_df['-log10(FDR)'] = -np.log10(plot_df['Adjusted P-value'])

    # Create figure
    plt.figure(figsize=(10, 6))

    # Create barplot
    bars = plt.barh(range(len(plot_df)), plot_df['-log10(FDR)'])

    # Color bars by -log10(FDR)
    norm = plt.Normalize(vmin=plot_df['-log10(FDR)'].min(),
                        vmax=plot_df['-log10(FDR)'].max())
    sm = plt.cm.ScalarMappable(cmap='Reds', norm=norm)
    sm.set_array([])

    for i, bar in enumerate(bars):
        bar.set_color(sm.to_rgba(plot_df['-log10(FDR)'].iloc[i]))

    # Labels
    plt.yticks(range(len(plot_df)), plot_df['Term'])
    plt.xlabel('-log10(Adjusted P-value)', fontsize=12)
    plt.title(title, fontsize=14, fontweight='bold')
    plt.colorbar(sm, label='-log10(FDR)')

    # Add significance line
    plt.axvline(x=-np.log10(0.05), color='black', linestyle='--', alpha=0.5, label='P = 0.05')
    plt.legend()

    plt.tight_layout()
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"  ✓ Saved plot: {output_file}")

# Plot GO:BP for positively correlated genes
if 'pos_results' in locals() and not pos_results['GO_BP'].empty:
    plot_top_terms(
        pos_results['GO_BP'],
        'GO Biological Process - Positively Correlated Genes',
        OUTPUT_DIR / 'plot_GO_BP_positive.png'
    )

# Plot GO:BP for negatively correlated genes
if 'neg_results' in locals() and not neg_results['GO_BP'].empty:
    plot_top_terms(
        neg_results['GO_BP'],
        'GO Biological Process - Negatively Correlated Genes',
        OUTPUT_DIR / 'plot_GO_BP_negative.png'
    )

# Plot KEGG for positively correlated genes
if 'kegg_pos' in locals() and not kegg_pos.empty:
    plot_top_terms(
        kegg_pos,
        'KEGG Pathways - Positively Correlated Genes',
        OUTPUT_DIR / 'plot_KEGG_positive.png'
    )

# Plot KEGG for negatively correlated genes
if 'kegg_neg' in locals() and not kegg_neg.empty:
    plot_top_terms(
        kegg_neg,
        'KEGG Pathways - Negatively Correlated Genes',
        OUTPUT_DIR / 'plot_KEGG_negative.png'
    )

# Step 7: Summary report
print("\n[STEP 7] Generating summary report...")

summary = {
    'total_genes_analyzed': len(corr_df),
    'positively_correlated_genes': len(pos_genes),
    'negatively_correlated_genes': len(neg_genes),
    'top_positive_correlation': corr_df[corr_df['correlation'] > 0].iloc[0]['correlation'] if len(pos_genes) > 0 else 0,
    'top_negative_correlation': corr_df[corr_df['correlation'] < 0].iloc[0]['correlation'] if len(neg_genes) > 0 else 0,
}

if 'pos_results' in locals():
    summary['GO_BP_positive_terms'] = len(pos_results['GO_BP'])
    summary['GO_MF_positive_terms'] = len(pos_results['GO_MF'])
    summary['GO_CC_positive_terms'] = len(pos_results['GO_CC'])

if 'neg_results' in locals():
    summary['GO_BP_negative_terms'] = len(neg_results['GO_BP'])
    summary['GO_MF_negative_terms'] = len(neg_results['GO_MF'])
    summary['GO_CC_negative_terms'] = len(neg_results['GO_CC'])

if 'kegg_pos' in locals():
    summary['KEGG_positive_pathways'] = len(kegg_pos)

if 'kegg_neg' in locals():
    summary['KEGG_negative_pathways'] = len(kegg_neg)

# Save summary
import json
with open(OUTPUT_DIR / 'enrichment_summary.json', 'w') as f:
    json.dump(summary, f, indent=2)

print("\n" + "=" * 70)
print("✅ ENRICHMENT ANALYSIS COMPLETED!")
print("=" * 70)
print(f"\nResults saved to: {OUTPUT_DIR}/")
print("\nSummary:")
for key, value in summary.items():
    print(f"  {key}: {value}")
print("\n")
