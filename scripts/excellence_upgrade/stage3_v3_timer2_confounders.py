#!/usr/bin/env python3
"""
Stage 3 v3: Partial Correlation with TIMER2.0 Immune Confounders
Uses real immune deconvolution scores from TIMER2.0

This version replaces the fallback method in stage3_v2 with proper
immune cell fraction estimates from TIMER2.0/xCell.

Author: Automated Pipeline
Date: 2025-11-02
"""

import pandas as pd
import numpy as np
from scipy import stats
from sklearn.linear_model import LinearRegression
from pathlib import Path
import json

# =============================================================================
# Configuration
# =============================================================================

BASE_DIR = Path(__file__).parent.parent.parent
DATA_DIR = BASE_DIR / "outputs" / "tcga_full_cohort_real"
TIMER_DIR = BASE_DIR / "outputs" / "timer2_results"
OUTPUT_DIR = BASE_DIR / "outputs" / "partial_correlation_v3_timer2"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Gene pairs to analyze
GENE_PAIRS = [
    ('CMTM6', 'STUB1'),
    ('CMTM6', 'SQSTM1'),
    ('STUB1', 'SQSTM1'),
    ('HIP1R', 'SQSTM1'),
    ('HIP1R', 'STUB1')
]

# =============================================================================
# Step 1: Load Data
# =============================================================================

print("\n" + "="*80)
print("PARTIAL CORRELATION v3 - WITH TIMER2.0 IMMUNE CONFOUNDERS")
print("="*80)

print("\n[LOAD] Loading expression data...")
expr_file = DATA_DIR / "expression_matrix_full_real.csv"
expr_df = pd.read_csv(expr_file)

# Set sample_id as index
if 'sample_id' in expr_df.columns:
    expr_df = expr_df.set_index('sample_id')

print(f"  Expression: {expr_df.shape[0]} samples x {expr_df.shape[1]} variables")

print("\n[LOAD] Loading TIMER2.0 immune scores...")
timer_file = TIMER_DIR / "timer2_immune_scores.csv"

if not timer_file.exists():
    print(f"  [ERROR] TIMER2.0 results not found: {timer_file}")
    print("  Please run: Rscript scripts/analysis/timer2_deconvolution.R")
    exit(1)

timer_df = pd.read_csv(timer_file)
print(f"  TIMER2.0: {timer_df.shape[0]} samples with immune scores")

# =============================================================================
# Step 2: Merge Expression and Immune Scores
# =============================================================================

print("\n[MERGE] Combining expression and immune data...")

# Merge on sample_id
timer_df = timer_df.set_index('sample_id')

# Find common samples
common_samples = expr_df.index.intersection(timer_df.index)
print(f"  Common samples: {len(common_samples)}")

expr_df = expr_df.loc[common_samples]
timer_df = timer_df.loc[common_samples]

# =============================================================================
# Step 3: Prepare Confounder Matrix
# =============================================================================

print("\n[CONFOUNDERS] Preparing confounder matrix...")

# Key immune confounders from TIMER2.0
confounder_cols = [
    'B_cell',           # B cell fraction
    'T_cell.CD4',       # CD4+ T cell fraction
    'T_cell.CD8',       # CD8+ T cell fraction
    'Neutrophil',       # Neutrophil fraction
    'Macrophage',       # Macrophage fraction
    'Myeloid.dendritic',# Dendritic cell fraction
    'T_cell_score',     # CD4 + CD8
    'Myeloid_score',    # Macrophage + Neutrophil + DC
    'Total_immune',     # Total immune infiltration
    'Tumor_purity',     # Tumor purity (1 - immune)
    'GEP_score'         # T-cell inflamed GEP
]

# Check which confounders are available
available_confounders = [col for col in confounder_cols if col in timer_df.columns]
print(f"  Available confounders: {len(available_confounders)}/{len(confounder_cols)}")

if not available_confounders:
    print("  [ERROR] No TIMER2.0 confounders available!")
    exit(1)

# Create confounder DataFrame
confounders_df = timer_df[available_confounders].copy()

# Z-score normalize confounders
confounders_df = (confounders_df - confounders_df.mean()) / confounders_df.std()

print(f"  Confounders ready: {confounders_df.shape[1]} variables")

# =============================================================================
# Step 4: Partial Correlation Function
# =============================================================================

def partial_correlation_regression(x, y, confounders):
    """
    Calculate partial correlation using regression residuals

    Args:
        x: Variable 1 (array-like)
        y: Variable 2 (array-like)
        confounders: Confounder matrix (DataFrame or 2D array)

    Returns:
        Partial correlation coefficient, p-value
    """
    # Remove NaN
    mask = ~(np.isnan(x) | np.isnan(y) | np.isnan(confounders).any(axis=1))
    x_clean = x[mask]
    y_clean = y[mask]
    conf_clean = confounders[mask]

    if len(x_clean) < 10:
        return np.nan, np.nan

    # Regress out confounders from x
    lr_x = LinearRegression()
    lr_x.fit(conf_clean, x_clean)
    x_residuals = x_clean - lr_x.predict(conf_clean)

    # Regress out confounders from y
    lr_y = LinearRegression()
    lr_y.fit(conf_clean, y_clean)
    y_residuals = y_clean - lr_y.predict(conf_clean)

    # Correlation of residuals = partial correlation
    r, p = stats.pearsonr(x_residuals, y_residuals)

    return r, p

def bootstrap_ci(x, y, confounders, n_bootstrap=1000, alpha=0.05):
    """
    Calculate bootstrap confidence interval for partial correlation

    Args:
        x: Variable 1
        y: Variable 2
        confounders: Confounder matrix
        n_bootstrap: Number of bootstrap samples
        alpha: Significance level

    Returns:
        Lower and upper CI bounds
    """
    n = len(x)
    partial_r_boot = []

    for _ in range(n_bootstrap):
        # Resample with replacement
        indices = np.random.choice(n, size=n, replace=True)
        x_boot = x[indices]
        y_boot = y[indices]
        conf_boot = confounders.iloc[indices] if isinstance(confounders, pd.DataFrame) else confounders[indices]

        # Calculate partial correlation
        r_boot, _ = partial_correlation_regression(x_boot, y_boot, conf_boot)

        if not np.isnan(r_boot):
            partial_r_boot.append(r_boot)

    if len(partial_r_boot) == 0:
        return np.nan, np.nan

    # Calculate percentile CI
    lower = np.percentile(partial_r_boot, alpha/2 * 100)
    upper = np.percentile(partial_r_boot, (1 - alpha/2) * 100)

    return lower, upper

# =============================================================================
# Step 5: Analyze Gene Pairs
# =============================================================================

print("\n[ANALYZE] Calculating partial correlations...")

results = []

for gene1, gene2 in GENE_PAIRS:
    print(f"\n--- {gene1} vs {gene2} ---")

    # Check if genes exist
    if gene1 not in expr_df.columns or gene2 not in expr_df.columns:
        print(f"  [SKIP] Genes not found in expression matrix")
        continue

    # Extract gene expression
    x = expr_df[gene1].values
    y = expr_df[gene2].values

    # Simple correlation (no confounders)
    mask_simple = ~(np.isnan(x) | np.isnan(y))
    r_simple, p_simple = stats.pearsonr(x[mask_simple], y[mask_simple])

    print(f"  Simple correlation:")
    print(f"    r = {r_simple:.3f}, P = {p_simple:.2e}")

    # Spearman correlation (non-parametric)
    rho_spearman, p_spearman = stats.spearmanr(x[mask_simple], y[mask_simple])
    print(f"    Spearman rho = {rho_spearman:.3f}, P = {p_spearman:.2e}")

    # Partial correlation (with immune confounders)
    r_partial, p_partial = partial_correlation_regression(x, y, confounders_df)

    print(f"\n  Partial correlation (controlling for immune infiltration):")
    print(f"    r = {r_partial:.3f}, P = {p_partial:.2e}")

    # Bootstrap CI
    print(f"  Calculating bootstrap 95% CI...")
    ci_lower, ci_upper = bootstrap_ci(x, y, confounders_df, n_bootstrap=1000)
    print(f"    95% CI = [{ci_lower:.3f}, {ci_upper:.3f}]")

    # Attenuation percentage
    attenuation = ((r_simple - r_partial) / r_simple * 100) if r_simple != 0 else 0
    print(f"    Attenuation: {attenuation:.1f}%")

    # Save results
    results.append({
        'gene1': gene1,
        'gene2': gene2,
        'simple_r': r_simple,
        'simple_p': p_simple,
        'spearman_rho': rho_spearman,
        'spearman_p': p_spearman,
        'partial_r': r_partial,
        'partial_p': p_partial,
        'partial_ci_lower': ci_lower,
        'partial_ci_upper': ci_upper,
        'attenuation_pct': attenuation,
        'n_samples': mask_simple.sum(),
        'confounders_used': ', '.join(available_confounders)
    })

# =============================================================================
# Step 6: Save Results
# =============================================================================

print("\n[SAVE] Writing results...")

# Save full results
results_df = pd.DataFrame(results)
output_file = OUTPUT_DIR / "partial_correlation_results_timer2.csv"
results_df.to_csv(output_file, index=False)
print(f"  Saved: {output_file}")

# Save JSON summary
summary = {
    'n_samples': int(expr_df.shape[0]),
    'n_gene_pairs': len(results),
    'confounders_used': available_confounders,
    'results': results
}

json_file = OUTPUT_DIR / "partial_correlation_summary_timer2.json"
with open(json_file, 'w') as f:
    json.dump(summary, f, indent=2)
print(f"  Saved: {json_file}")

# =============================================================================
# Step 7: Comparison with Stage 3 v2 (Fallback Method)
# =============================================================================

print("\n[COMPARE] Comparing with v2 fallback method...")

v2_file = BASE_DIR / "outputs" / "partial_correlation_v2_fixed" / "partial_correlation_results.csv"

if v2_file.exists():
    v2_df = pd.read_csv(v2_file)

    # Merge with v3 results
    comparison_df = results_df.merge(
        v2_df[['gene1', 'gene2', 'partial_r', 'partial_p']],
        on=['gene1', 'gene2'],
        suffixes=('_timer2', '_fallback')
    )

    # Calculate difference
    comparison_df['r_difference'] = comparison_df['partial_r_timer2'] - comparison_df['partial_r_fallback']

    print("\n  Comparison of partial correlations:")
    print(comparison_df[['gene1', 'gene2', 'partial_r_fallback', 'partial_r_timer2', 'r_difference']])

    # Save comparison
    comp_file = OUTPUT_DIR / "v2_vs_v3_comparison.csv"
    comparison_df.to_csv(comp_file, index=False)
    print(f"\n  Saved comparison: {comp_file}")
else:
    print("  v2 results not found, skipping comparison")

# =============================================================================
# Final Summary
# =============================================================================

print("\n" + "="*80)
print("PARTIAL CORRELATION v3 COMPLETE")
print("="*80)

print("\nKey findings:")
for idx, row in results_df.iterrows():
    print(f"\n{row['gene1']}-{row['gene2']}:")
    print(f"  Simple r = {row['simple_r']:.3f} (P={row['simple_p']:.2e})")
    print(f"  Partial r = {row['partial_r']:.3f} (P={row['partial_p']:.2e})")
    print(f"  95% CI = [{row['partial_ci_lower']:.3f}, {row['partial_ci_upper']:.3f}]")
    print(f"  Attenuation = {row['attenuation_pct']:.1f}%")

print("\n" + "="*80)
print("Next step:")
print("  Review results and proceed to single-cell validation")
print("="*80)
