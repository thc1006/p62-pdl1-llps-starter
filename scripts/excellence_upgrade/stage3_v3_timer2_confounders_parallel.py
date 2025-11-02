#!/usr/bin/env python3
"""
Stage 3 v3: Parallel Partial Correlation with TIMER2.0 - 32-Core Optimized
Uses joblib to leverage all 32 CPU cores for bootstrap parallelization

Parallelization Strategy:
- Level 1: Gene pairs analyzed in parallel (5 pairs)
- Level 2: Bootstrap iterations parallelized (1000 per pair)
- Total: Up to 32x speedup on 32-core system

Author: Automated Pipeline
Date: 2025-11-02
"""

import pandas as pd
import numpy as np
from scipy import stats
from sklearn.linear_model import LinearRegression
from pathlib import Path
import json
from joblib import Parallel, delayed
import multiprocessing as mp
import time
import mygene

# =============================================================================
# Configuration
# =============================================================================

BASE_DIR = Path(__file__).parent.parent.parent
DATA_DIR = BASE_DIR / "outputs" / "tcga_full_cohort_real"
TIMER_DIR = BASE_DIR / "outputs" / "timer2_results"
OUTPUT_DIR = BASE_DIR / "outputs" / "partial_correlation_v3_timer2_parallel"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Use all available cores
N_CORES = mp.cpu_count()
print(f"System has {N_CORES} CPU cores available")

# Gene pairs to analyze (using gene symbols)
GENE_PAIRS = [
    ('CMTM6', 'STUB1'),
    ('CMTM6', 'SQSTM1'),
    ('STUB1', 'SQSTM1'),
    ('HIP1R', 'SQSTM1'),
    ('HIP1R', 'STUB1')
]

# =============================================================================
# Gene Symbol to Ensembl ID Conversion
# =============================================================================

def convert_symbols_to_ensembl(gene_symbols):
    """
    Convert gene symbols to Ensembl IDs using MyGene.info API
    with fallback to hardcoded mappings for known problematic genes

    Args:
        gene_symbols: List of gene symbols

    Returns:
        Dictionary mapping symbols to Ensembl IDs
    """
    print("\n[GENE MAPPING] Converting gene symbols to Ensembl IDs...")

    # Hardcoded mappings for genes with known MyGene.info issues
    FALLBACK_MAPPINGS = {
        'SQSTM1': 'ENSG00000161011',  # p62, verified from NCBI/Ensembl
        'CD274': 'ENSG00000120217',   # PD-L1
    }

    mg = mygene.MyGeneInfo()

    # Query MyGene.info
    results = mg.querymany(
        gene_symbols,
        scopes='symbol',
        fields='ensembl.gene',
        species='human',
        verbose=False
    )

    # Process results
    mapping = {}
    not_found = []

    for result in results:
        query_symbol = result.get('query')

        if result.get('notfound'):
            # Try fallback mapping
            if query_symbol in FALLBACK_MAPPINGS:
                mapping[query_symbol] = FALLBACK_MAPPINGS[query_symbol]
                print(f"  {query_symbol} -> {FALLBACK_MAPPINGS[query_symbol]} (fallback)")
            else:
                not_found.append(query_symbol)
        elif 'ensembl' in result and 'gene' in result['ensembl']:
            ensembl_id = result['ensembl']['gene']
            mapping[query_symbol] = ensembl_id
            print(f"  {query_symbol} -> {ensembl_id}")
        else:
            # Try fallback mapping if MyGene.info doesn't return ensembl field
            if query_symbol in FALLBACK_MAPPINGS:
                mapping[query_symbol] = FALLBACK_MAPPINGS[query_symbol]
                print(f"  {query_symbol} -> {FALLBACK_MAPPINGS[query_symbol]} (fallback)")
            else:
                not_found.append(query_symbol)

    if not_found:
        print(f"\n  [WARNING] Could not map: {', '.join(not_found)}")

    return mapping

# =============================================================================
# Step 1: Load Data
# =============================================================================

print("\n" + "="*80)
print("PARALLEL PARTIAL CORRELATION v3 - WITH TIMER2.0 IMMUNE CONFOUNDERS")
print(f"Using {N_CORES} CPU cores for acceleration")
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
# NOTE: TIMER2.0 uses 'ID' column for UUID, not 'sample_id' (which contains row numbers)
if 'ID' in timer_df.columns:
    timer_df = timer_df.set_index('ID')
elif 'sample_id' in timer_df.columns:
    # Fallback: check if sample_id contains UUIDs (length > 30)
    if timer_df['sample_id'].astype(str).str.len().mean() > 30:
        timer_df = timer_df.set_index('sample_id')
    else:
        print("[ERROR] TIMER2.0 data has no valid sample ID column!")
        exit(1)

# Find common samples
common_samples = expr_df.index.intersection(timer_df.index)
print(f"  Common samples: {len(common_samples)}")

expr_df = expr_df.loc[common_samples]
timer_df = timer_df.loc[common_samples]

# =============================================================================
# Step 2.5: Map Gene Symbols to Ensembl IDs
# =============================================================================

# Collect all unique gene symbols from gene pairs
all_gene_symbols = set()
for gene1, gene2 in GENE_PAIRS:
    all_gene_symbols.add(gene1)
    all_gene_symbols.add(gene2)

# Convert symbols to Ensembl IDs
symbol_to_ensembl = convert_symbols_to_ensembl(list(all_gene_symbols))

# Create reverse mapping for results
ensembl_to_symbol = {v: k for k, v in symbol_to_ensembl.items()}

print(f"\n  Successfully mapped {len(symbol_to_ensembl)}/{len(all_gene_symbols)} genes")

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

# Remove confounders that are all NaN
valid_confounders = []
for col in available_confounders:
    if not confounders_df[col].isna().all():
        valid_confounders.append(col)
    else:
        print(f"  [WARNING] Removing confounder '{col}' (all NaN)")

if not valid_confounders:
    print("  [ERROR] No valid TIMER2.0 confounders (all are NaN)!")
    exit(1)

confounders_df = confounders_df[valid_confounders]
available_confounders = valid_confounders

# Z-score normalize confounders
confounders_df = (confounders_df - confounders_df.mean()) / confounders_df.std()

print(f"  Confounders ready: {confounders_df.shape[1]} variables")

# =============================================================================
# Step 4: Parallel Partial Correlation Functions
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

def single_bootstrap_iteration(x, y, confounders, seed):
    """
    Single bootstrap iteration (for parallel execution)

    Args:
        x: Variable 1
        y: Variable 2
        confounders: Confounder matrix
        seed: Random seed for reproducibility

    Returns:
        Bootstrap partial correlation
    """
    np.random.seed(seed)
    n = len(x)

    # Resample with replacement
    indices = np.random.choice(n, size=n, replace=True)
    x_boot = x[indices]
    y_boot = y[indices]
    conf_boot = confounders.iloc[indices] if isinstance(confounders, pd.DataFrame) else confounders[indices]

    # Calculate partial correlation
    r_boot, _ = partial_correlation_regression(x_boot, y_boot, conf_boot)

    return r_boot

def bootstrap_ci_parallel(x, y, confounders, n_bootstrap=1000, alpha=0.05, n_jobs=-1):
    """
    Parallel bootstrap confidence interval for partial correlation

    Args:
        x: Variable 1
        y: Variable 2
        confounders: Confounder matrix
        n_bootstrap: Number of bootstrap samples
        alpha: Significance level
        n_jobs: Number of parallel jobs (-1 = all cores)

    Returns:
        Lower and upper CI bounds
    """
    print(f"      Running {n_bootstrap} bootstrap iterations on {N_CORES} cores...", end='', flush=True)
    start_time = time.time()

    # Generate seeds for reproducibility
    seeds = np.random.randint(0, 1000000, size=n_bootstrap)

    # Parallel bootstrap
    partial_r_boot = Parallel(n_jobs=n_jobs, backend='loky')(
        delayed(single_bootstrap_iteration)(x, y, confounders, seed)
        for seed in seeds
    )

    # Filter out NaN values
    partial_r_boot = [r for r in partial_r_boot if not np.isnan(r)]

    elapsed = time.time() - start_time
    print(f" done in {elapsed:.1f}s")

    if len(partial_r_boot) == 0:
        return np.nan, np.nan

    # Calculate percentile CI
    lower = np.percentile(partial_r_boot, alpha/2 * 100)
    upper = np.percentile(partial_r_boot, (1 - alpha/2) * 100)

    return lower, upper

def analyze_gene_pair(gene1, gene2, expr_df, confounders_df, available_confounders, symbol_to_ensembl):
    """
    Analyze a single gene pair (for parallel execution)

    Args:
        gene1: First gene symbol
        gene2: Second gene symbol
        expr_df: Expression DataFrame (with Ensembl IDs as columns)
        confounders_df: Confounder DataFrame
        available_confounders: List of confounder names
        symbol_to_ensembl: Dictionary mapping symbols to Ensembl IDs

    Returns:
        Dictionary with analysis results
    """
    print(f"\n--- {gene1} vs {gene2} ---")

    # Map symbols to Ensembl IDs
    gene1_ensembl = symbol_to_ensembl.get(gene1)
    gene2_ensembl = symbol_to_ensembl.get(gene2)

    if gene1_ensembl is None or gene2_ensembl is None:
        print(f"  [SKIP] Could not map gene symbols to Ensembl IDs")
        print(f"    {gene1}: {'✓' if gene1_ensembl else '✗'}")
        print(f"    {gene2}: {'✓' if gene2_ensembl else '✗'}")
        return None

    # Check if genes exist in expression matrix
    if gene1_ensembl not in expr_df.columns or gene2_ensembl not in expr_df.columns:
        print(f"  [SKIP] Ensembl IDs not found in expression matrix")
        print(f"    {gene1} ({gene1_ensembl}): {'✓' if gene1_ensembl in expr_df.columns else '✗'}")
        print(f"    {gene2} ({gene2_ensembl}): {'✓' if gene2_ensembl in expr_df.columns else '✗'}")
        return None

    print(f"  Analyzing: {gene1} ({gene1_ensembl}) vs {gene2} ({gene2_ensembl})")

    # Extract gene expression using Ensembl IDs
    x = expr_df[gene1_ensembl].values
    y = expr_df[gene2_ensembl].values

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

    # Parallel Bootstrap CI
    print(f"  Parallel bootstrap 95% CI:")
    ci_lower, ci_upper = bootstrap_ci_parallel(x, y, confounders_df, n_bootstrap=1000, n_jobs=-1)
    print(f"    95% CI = [{ci_lower:.3f}, {ci_upper:.3f}]")

    # Attenuation percentage
    attenuation = ((r_simple - r_partial) / r_simple * 100) if r_simple != 0 else 0
    print(f"    Attenuation: {attenuation:.1f}%")

    return {
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
    }

# =============================================================================
# Step 5: Parallel Gene Pair Analysis
# =============================================================================

print("\n[ANALYZE] Calculating partial correlations (parallel mode)...")
print(f"  Analyzing {len(GENE_PAIRS)} gene pairs")
print(f"  Each pair: 1,000 bootstrap iterations")
print(f"  Total computational load: {len(GENE_PAIRS) * 1000} = {len(GENE_PAIRS) * 1000:,} iterations")
print(f"  Parallelization: {N_CORES} cores\n")

overall_start = time.time()

# Option 1: Sequential gene pairs, parallel bootstrap (better for memory)
# This processes gene pairs one-by-one but parallelizes the bootstrap within each
results = []
for gene1, gene2 in GENE_PAIRS:
    result = analyze_gene_pair(gene1, gene2, expr_df, confounders_df, available_confounders, symbol_to_ensembl)
    if result is not None:
        results.append(result)

overall_elapsed = time.time() - overall_start
print(f"\n[PERFORMANCE] Total analysis time: {overall_elapsed:.1f}s")
if len(results) > 0:
    print(f"  Average per gene pair: {overall_elapsed/len(results):.1f}s")
else:
    print(f"  [WARNING] No results generated - check gene names and sample matching")

# =============================================================================
# Step 6: Save Results
# =============================================================================

print("\n[SAVE] Writing results...")

# Save full results
results_df = pd.DataFrame(results)
output_file = OUTPUT_DIR / "partial_correlation_results_timer2_parallel.csv"
results_df.to_csv(output_file, index=False)
print(f"  Saved: {output_file}")

# Save JSON summary with NumPy type converter
class NumpyEncoder(json.JSONEncoder):
    """Custom JSON encoder for NumPy types"""
    def default(self, obj):
        if isinstance(obj, (np.integer, np.int64)):
            return int(obj)
        elif isinstance(obj, (np.floating, np.float64)):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        return super().default(obj)

summary = {
    'n_samples': int(expr_df.shape[0]),
    'n_gene_pairs': len(results),
    'n_cores_used': int(N_CORES),
    'total_time_seconds': float(overall_elapsed),
    'confounders_used': available_confounders,
    'results': results
}

json_file = OUTPUT_DIR / "partial_correlation_summary_timer2_parallel.json"
with open(json_file, 'w') as f:
    json.dump(summary, f, indent=2, cls=NumpyEncoder)
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
    comp_file = OUTPUT_DIR / "v2_vs_v3_comparison_parallel.csv"
    comparison_df.to_csv(comp_file, index=False)
    print(f"\n  Saved comparison: {comp_file}")
else:
    print("  v2 results not found, skipping comparison")

# =============================================================================
# Final Summary
# =============================================================================

print("\n" + "="*80)
print("PARALLEL PARTIAL CORRELATION v3 COMPLETE")
print("="*80)

print(f"\nPerformance summary:")
print(f"  CPU cores used: {N_CORES}")
print(f"  Total iterations: {len(results) * 1000:,}")
print(f"  Total time: {overall_elapsed:.1f}s")
print(f"  Throughput: {(len(results) * 1000) / overall_elapsed:.0f} iterations/second")

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
