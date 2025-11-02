#!/usr/bin/env python3
"""
Debug script to understand why partial correlation returns NaN
"""

import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.linear_model import LinearRegression
from scipy import stats

# Paths
EXPR_FILE = Path("outputs/tcga_full_cohort_real/expression_matrix_full_real.csv")
TIMER_FILE = Path("outputs/timer2_results/timer2_immune_scores.csv")

print("=" * 80)
print("DEBUG: Partial Correlation NaN Issue")
print("=" * 80)

# Load data
print("\n[1] Loading data...")
expr_df = pd.read_csv(EXPR_FILE)
if 'sample_id' in expr_df.columns:
    expr_df = expr_df.set_index('sample_id')
print(f"  Expression: {expr_df.shape}")

timer_df = pd.read_csv(TIMER_FILE)
if 'ID' in timer_df.columns:
    timer_df = timer_df.set_index('ID')
print(f"  TIMER2.0: {timer_df.shape}")

# Merge
common_samples = expr_df.index.intersection(timer_df.index)
print(f"  Common samples: {len(common_samples)}")

expr_df = expr_df.loc[common_samples]
timer_df = timer_df.loc[common_samples]

# Check confounders
confounder_cols = [
    'B_cell', 'T_cell.CD4', 'T_cell.CD8', 'Neutrophil',
    'Macrophage', 'Myeloid.dendritic', 'T_cell_score',
    'Myeloid_score', 'Total_immune', 'Tumor_purity', 'GEP_score'
]

print("\n[2] Checking confounder data...")
confounders_df = timer_df[confounder_cols].copy()
print(f"  Confounder matrix shape: {confounders_df.shape}")
print(f"  Data types:\n{confounders_df.dtypes}")
print(f"\n  Summary statistics:")
print(confounders_df.describe())
print(f"\n  NaN counts:")
print(confounders_df.isna().sum())
print(f"\n  First 5 rows:")
print(confounders_df.head())

# Test with real genes
print("\n[3] Testing partial correlation with CMTM6 vs STUB1...")
gene1_id = "ENSG00000091317"  # CMTM6
gene2_id = "ENSG00000103266"  # STUB1

if gene1_id in expr_df.columns and gene2_id in expr_df.columns:
    x = expr_df[gene1_id].values
    y = expr_df[gene2_id].values
    confounders = confounders_df.values

    print(f"  Gene 1 (CMTM6): shape={x.shape}, mean={np.mean(x):.3f}, std={np.std(x):.3f}")
    print(f"  Gene 2 (STUB1): shape={y.shape}, mean={np.mean(y):.3f}, std={np.std(y):.3f}")
    print(f"  Confounders: shape={confounders.shape}")

    # Check for NaN
    print(f"\n  NaN in gene 1: {np.isnan(x).sum()}")
    print(f"  NaN in gene 2: {np.isnan(y).sum()}")
    print(f"  NaN in confounders: {np.isnan(confounders).sum()}")

    # Remove NaN
    mask = ~(np.isnan(x) | np.isnan(y) | np.isnan(confounders).any(axis=1))
    x_clean = x[mask]
    y_clean = y[mask]
    conf_clean = confounders[mask]

    print(f"\n  After removing NaN: {len(x_clean)} samples")

    if len(x_clean) >= 10:
        # Test regression
        print("\n  Testing LinearRegression for x...")
        lr_x = LinearRegression()
        try:
            lr_x.fit(conf_clean, x_clean)
            x_pred = lr_x.predict(conf_clean)
            x_residuals = x_clean - x_pred
            print(f"    Fitted successfully!")
            print(f"    R² = {lr_x.score(conf_clean, x_clean):.4f}")
            print(f"    Residuals: mean={np.mean(x_residuals):.6f}, std={np.std(x_residuals):.6f}")
            print(f"    Residuals contain NaN: {np.isnan(x_residuals).any()}")
        except Exception as e:
            print(f"    ERROR: {e}")

        print("\n  Testing LinearRegression for y...")
        lr_y = LinearRegression()
        try:
            lr_y.fit(conf_clean, y_clean)
            y_pred = lr_y.predict(conf_clean)
            y_residuals = y_clean - y_pred
            print(f"    Fitted successfully!")
            print(f"    R² = {lr_y.score(conf_clean, y_clean):.4f}")
            print(f"    Residuals: mean={np.mean(y_residuals):.6f}, std={np.std(y_residuals):.6f}")
            print(f"    Residuals contain NaN: {np.isnan(y_residuals).any()}")
        except Exception as e:
            print(f"    ERROR: {e}")

        # Test correlation
        print("\n  Testing correlation of residuals...")
        try:
            r, p = stats.pearsonr(x_residuals, y_residuals)
            print(f"    Partial correlation: r = {r:.4f}, p = {p:.4e}")
        except Exception as e:
            print(f"    ERROR: {e}")
    else:
        print(f"  ERROR: Not enough samples ({len(x_clean)} < 10)")
else:
    print(f"  ERROR: Genes not found in expression matrix")
    print(f"    {gene1_id} in columns: {gene1_id in expr_df.columns}")
    print(f"    {gene2_id} in columns: {gene2_id in expr_df.columns}")

print("\n" + "=" * 80)
print("DEBUG COMPLETE")
print("=" * 80)
