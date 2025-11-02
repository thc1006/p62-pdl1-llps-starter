#!/usr/bin/env python3
"""
Sensitivity Analysis for Robustness Testing
Tests if correlations are stable across:
1. Different cancer types (LUAD vs LUSC vs SKCM)
2. Outlier exclusion strategies
3. Different statistical methods
4. Bootstrap resampling

Author: Automated Pipeline
Date: 2025-11-02
"""

import pandas as pd
import numpy as np
from scipy import stats
from sklearn.preprocessing import RobustScaler
from pathlib import Path
import json

# =============================================================================
# Configuration
# =============================================================================

BASE_DIR = Path(__file__).parent.parent.parent
DATA_DIR = BASE_DIR / "outputs" / "tcga_full_cohort_real"
OUTPUT_DIR = BASE_DIR / "outputs" / "sensitivity_analysis"

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
print("SENSITIVITY ANALYSIS PIPELINE")
print("="*80)

print("\n[LOAD] Loading expression data...")
expr_file = DATA_DIR / "expression_matrix_full_real.csv"
expr_df = pd.read_csv(expr_file)

# Set sample_id as index
if 'sample_id' in expr_df.columns:
    sample_ids = expr_df['sample_id']
    expr_df = expr_df.set_index('sample_id')
else:
    sample_ids = expr_df.index

# Extract cancer type
cancer_type = expr_df['cancer_type']
expr_df = expr_df.drop('cancer_type', axis=1)

print(f"  Expression: {expr_df.shape[0]} samples x {expr_df.shape[1]} genes")

# =============================================================================
# Step 2: Per-Cancer Type Analysis
# =============================================================================

def analyze_per_cancer_type(expr_df: pd.DataFrame, cancer_type: pd.Series) -> pd.DataFrame:
    """
    Calculate correlations separately for each cancer type

    Args:
        expr_df: Expression DataFrame
        cancer_type: Cancer type labels

    Returns:
        Results DataFrame
    """
    print("\n[PER-CANCER] Analyzing by cancer type...")

    results = []

    for cancer in cancer_type.unique():
        print(f"\n  --- {cancer} ---")

        # Subset to cancer type
        mask = cancer_type == cancer
        subset_df = expr_df[mask]

        print(f"    N samples: {len(subset_df)}")

        for gene1, gene2 in GENE_PAIRS:
            if gene1 not in subset_df.columns or gene2 not in subset_df.columns:
                continue

            x = subset_df[gene1].values
            y = subset_df[gene2].values

            # Remove NaN
            mask_valid = ~(np.isnan(x) | np.isnan(y))
            x_clean = x[mask_valid]
            y_clean = y[mask_valid]

            if len(x_clean) < 10:
                continue

            # Pearson
            r, p = stats.pearsonr(x_clean, y_clean)

            # Spearman
            rho, p_spearman = stats.spearmanr(x_clean, y_clean)

            print(f"    {gene1}-{gene2}: r={r:.3f} (P={p:.2e})")

            results.append({
                'cancer_type': cancer,
                'gene1': gene1,
                'gene2': gene2,
                'n_samples': len(x_clean),
                'pearson_r': r,
                'pearson_p': p,
                'spearman_rho': rho,
                'spearman_p': p_spearman
            })

    return pd.DataFrame(results)

# =============================================================================
# Step 3: Outlier Exclusion Strategies
# =============================================================================

def analyze_with_outlier_exclusion(expr_df: pd.DataFrame, method: str) -> pd.DataFrame:
    """
    Analyze after removing outliers

    Args:
        expr_df: Expression DataFrame
        method: 'zscore' or 'iqr' or 'robust'

    Returns:
        Results DataFrame
    """
    print(f"\n[OUTLIER] Analyzing with {method} outlier exclusion...")

    expr_clean = expr_df.copy()

    if method == 'zscore':
        # Remove samples with z-score > 3 in any gene
        z_scores = np.abs((expr_clean - expr_clean.mean()) / expr_clean.std())
        outlier_mask = (z_scores > 3).any(axis=1)
        expr_clean = expr_clean[~outlier_mask]
        print(f"  Removed {outlier_mask.sum()} outlier samples (z-score > 3)")

    elif method == 'iqr':
        # Remove samples outside 1.5 * IQR
        Q1 = expr_clean.quantile(0.25, axis=0)
        Q3 = expr_clean.quantile(0.75, axis=0)
        IQR = Q3 - Q1

        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR

        outlier_mask = ((expr_clean < lower_bound) | (expr_clean > upper_bound)).any(axis=1)
        expr_clean = expr_clean[~outlier_mask]
        print(f"  Removed {outlier_mask.sum()} outlier samples (IQR method)")

    elif method == 'robust':
        # Robust scaling (median + MAD)
        scaler = RobustScaler()
        expr_scaled = pd.DataFrame(
            scaler.fit_transform(expr_clean),
            index=expr_clean.index,
            columns=expr_clean.columns
        )

        outlier_mask = (np.abs(expr_scaled) > 3).any(axis=1)
        expr_clean = expr_clean[~outlier_mask]
        print(f"  Removed {outlier_mask.sum()} outlier samples (robust scaling)")

    # Calculate correlations
    results = []

    for gene1, gene2 in GENE_PAIRS:
        if gene1 not in expr_clean.columns or gene2 not in expr_clean.columns:
            continue

        x = expr_clean[gene1].values
        y = expr_clean[gene2].values

        mask_valid = ~(np.isnan(x) | np.isnan(y))
        x_clean = x[mask_valid]
        y_clean = y[mask_valid]

        if len(x_clean) < 10:
            continue

        r, p = stats.pearsonr(x_clean, y_clean)
        rho, p_spearman = stats.spearmanr(x_clean, y_clean)

        results.append({
            'method': method,
            'gene1': gene1,
            'gene2': gene2,
            'n_samples': len(x_clean),
            'pearson_r': r,
            'pearson_p': p,
            'spearman_rho': rho,
            'spearman_p': p_spearman
        })

    return pd.DataFrame(results)

# =============================================================================
# Step 4: Bootstrap Stability Analysis
# =============================================================================

def bootstrap_stability(expr_df: pd.DataFrame, n_bootstrap=1000) -> pd.DataFrame:
    """
    Test correlation stability via bootstrap

    Args:
        expr_df: Expression DataFrame
        n_bootstrap: Number of bootstrap samples

    Returns:
        Bootstrap results DataFrame
    """
    print(f"\n[BOOTSTRAP] Testing stability with {n_bootstrap} resamples...")

    results = []

    for gene1, gene2 in GENE_PAIRS:
        if gene1 not in expr_df.columns or gene2 not in expr_df.columns:
            continue

        print(f"  {gene1}-{gene2}...")

        x = expr_df[gene1].values
        y = expr_df[gene2].values

        mask_valid = ~(np.isnan(x) | np.isnan(y))
        x_clean = x[mask_valid]
        y_clean = y[mask_valid]

        if len(x_clean) < 10:
            continue

        # Bootstrap
        boot_r = []

        for _ in range(n_bootstrap):
            indices = np.random.choice(len(x_clean), size=len(x_clean), replace=True)
            x_boot = x_clean[indices]
            y_boot = y_clean[indices]

            r_boot, _ = stats.pearsonr(x_boot, y_boot)
            boot_r.append(r_boot)

        # Statistics
        boot_r = np.array(boot_r)
        mean_r = boot_r.mean()
        std_r = boot_r.std()
        ci_lower = np.percentile(boot_r, 2.5)
        ci_upper = np.percentile(boot_r, 97.5)

        # Stability: coefficient of variation
        cv = std_r / abs(mean_r) if mean_r != 0 else np.inf

        print(f"    Mean r = {mean_r:.3f} +/- {std_r:.3f}")
        print(f"    95% CI = [{ci_lower:.3f}, {ci_upper:.3f}]")
        print(f"    CV = {cv:.3f}")

        results.append({
            'gene1': gene1,
            'gene2': gene2,
            'n_samples': len(x_clean),
            'mean_r': mean_r,
            'std_r': std_r,
            'ci_lower': ci_lower,
            'ci_upper': ci_upper,
            'cv': cv,
            'n_bootstrap': n_bootstrap
        })

    return pd.DataFrame(results)

# =============================================================================
# Step 5: Alternative Correlation Methods
# =============================================================================

def test_alternative_methods(expr_df: pd.DataFrame) -> pd.DataFrame:
    """
    Test different correlation methods

    Args:
        expr_df: Expression DataFrame

    Returns:
        Results DataFrame
    """
    print("\n[METHODS] Testing alternative correlation methods...")

    results = []

    for gene1, gene2 in GENE_PAIRS:
        if gene1 not in expr_df.columns or gene2 not in expr_df.columns:
            continue

        x = expr_df[gene1].values
        y = expr_df[gene2].values

        mask_valid = ~(np.isnan(x) | np.isnan(y))
        x_clean = x[mask_valid]
        y_clean = y[mask_valid]

        if len(x_clean) < 10:
            continue

        # Pearson
        r_pearson, p_pearson = stats.pearsonr(x_clean, y_clean)

        # Spearman
        r_spearman, p_spearman = stats.spearmanr(x_clean, y_clean)

        # Kendall's tau
        tau, p_kendall = stats.kendalltau(x_clean, y_clean)

        print(f"  {gene1}-{gene2}:")
        print(f"    Pearson: r={r_pearson:.3f}")
        print(f"    Spearman: rho={r_spearman:.3f}")
        print(f"    Kendall: tau={tau:.3f}")

        results.append({
            'gene1': gene1,
            'gene2': gene2,
            'n_samples': len(x_clean),
            'pearson_r': r_pearson,
            'pearson_p': p_pearson,
            'spearman_rho': r_spearman,
            'spearman_p': p_spearman,
            'kendall_tau': tau,
            'kendall_p': p_kendall
        })

    return pd.DataFrame(results)

# =============================================================================
# Main Pipeline
# =============================================================================

def main():
    """
    Main execution pipeline
    """
    # Analysis 1: Per-cancer type
    per_cancer_results = analyze_per_cancer_type(expr_df, cancer_type)

    # Analysis 2: Outlier exclusion
    outlier_results = []
    for method in ['zscore', 'iqr', 'robust']:
        results = analyze_with_outlier_exclusion(expr_df, method)
        outlier_results.append(results)
    outlier_results = pd.concat(outlier_results, ignore_index=True)

    # Analysis 3: Bootstrap stability
    bootstrap_results = bootstrap_stability(expr_df, n_bootstrap=1000)

    # Analysis 4: Alternative methods
    methods_results = test_alternative_methods(expr_df)

    # Save results
    print("\n[SAVE] Writing results...")

    # Per-cancer
    per_cancer_file = OUTPUT_DIR / "per_cancer_type_results.csv"
    per_cancer_results.to_csv(per_cancer_file, index=False)
    print(f"  Saved: {per_cancer_file}")

    # Outlier exclusion
    outlier_file = OUTPUT_DIR / "outlier_exclusion_results.csv"
    outlier_results.to_csv(outlier_file, index=False)
    print(f"  Saved: {outlier_file}")

    # Bootstrap
    bootstrap_file = OUTPUT_DIR / "bootstrap_stability_results.csv"
    bootstrap_results.to_csv(bootstrap_file, index=False)
    print(f"  Saved: {bootstrap_file}")

    # Methods comparison
    methods_file = OUTPUT_DIR / "methods_comparison_results.csv"
    methods_results.to_csv(methods_file, index=False)
    print(f"  Saved: {methods_file}")

    # Summary JSON
    summary = {
        'per_cancer_results': per_cancer_results.to_dict('records'),
        'outlier_exclusion': outlier_results.to_dict('records'),
        'bootstrap_stability': bootstrap_results.to_dict('records'),
        'methods_comparison': methods_results.to_dict('records')
    }

    json_file = OUTPUT_DIR / "sensitivity_analysis_summary.json"
    with open(json_file, 'w') as f:
        json.dump(summary, f, indent=2)
    print(f"  Saved: {json_file}")

    # Final summary
    print("\n" + "="*80)
    print("SENSITIVITY ANALYSIS COMPLETE")
    print("="*80)

    print("\nKey findings:")
    print("\n1. Per-cancer type consistency:")
    for _, row in per_cancer_results.iterrows():
        print(f"  {row['cancer_type']} - {row['gene1']}-{row['gene2']}: r={row['pearson_r']:.3f}")

    print("\n2. Bootstrap stability:")
    for _, row in bootstrap_results.iterrows():
        print(f"  {row['gene1']}-{row['gene2']}: CV={row['cv']:.3f} (lower is more stable)")

    print("\n" + "="*80)
    print("Next step:")
    print("  Run: python scripts/figures/generate_all_figures.py")
    print("="*80)

if __name__ == "__main__":
    main()
