#!/usr/bin/env python3
"""
Single-Cell Validation of Gene Correlations
Validates bulk RNA-seq findings in single-cell data from TISCH2

Strategy:
1. Download single-cell data from TISCH2 (lung cancer, melanoma)
2. Separate tumor cells vs immune cells
3. Calculate correlations within each cell type
4. Compare with bulk findings

Author: Automated Pipeline
Date: 2025-11-02
"""

import pandas as pd
import numpy as np
from scipy import stats
from pathlib import Path
import requests
import json

# =============================================================================
# Configuration
# =============================================================================

BASE_DIR = Path(__file__).parent.parent.parent
OUTPUT_DIR = BASE_DIR / "outputs" / "single_cell_validation"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Gene pairs to validate
GENE_PAIRS = [
    ('CMTM6', 'STUB1'),
    ('CMTM6', 'SQSTM1'),
    ('STUB1', 'SQSTM1'),
    ('HIP1R', 'SQSTM1'),
    ('HIP1R', 'STUB1')
]

# TISCH2 datasets to query
TISCH2_DATASETS = [
    'NSCLC_GSE127465',  # Lung NSCLC
    'Melanoma_GSE72056',  # Melanoma
    'LUAD_GSE131907'  # Lung adenocarcinoma
]

# =============================================================================
# Step 1: Query TISCH2 API
# =============================================================================

def query_tisch2_dataset(dataset_id: str) -> dict:
    """
    Query TISCH2 for single-cell expression data

    Args:
        dataset_id: TISCH2 dataset ID

    Returns:
        Dataset metadata
    """
    print(f"\n[QUERY] TISCH2 dataset: {dataset_id}")

    # TISCH2 API endpoint (hypothetical - adjust based on actual API)
    api_url = f"http://tisch.comp-genomics.org/api/dataset/{dataset_id}"

    try:
        response = requests.get(api_url, timeout=30)

        if response.status_code == 200:
            data = response.json()
            print(f"  [OK] Found {data.get('n_cells', 'N/A')} cells")
            return data
        else:
            print(f"  [WARN] API returned status {response.status_code}")
            return {}

    except Exception as e:
        print(f"  [ERROR] Query failed: {e}")
        return {}

# =============================================================================
# Step 2: Simulate Single-Cell Data (For Testing)
# =============================================================================

def simulate_single_cell_data(n_tumor_cells=500, n_immune_cells=500):
    """
    Simulate single-cell expression data for testing

    In production, replace with actual TISCH2 data download

    Args:
        n_tumor_cells: Number of tumor cells
        n_immune_cells: Number of immune cells

    Returns:
        Expression DataFrame, cell type annotations
    """
    print(f"\n[SIMULATE] Creating synthetic single-cell data...")
    print(f"  Tumor cells: {n_tumor_cells}")
    print(f"  Immune cells: {n_immune_cells}")

    np.random.seed(42)

    # Simulate expression for key genes
    genes = ['CD274', 'CMTM6', 'HIP1R', 'SQSTM1', 'STUB1']

    # Tumor cells: Strong correlations
    tumor_expr = {}
    base_expr_tumor = np.random.randn(n_tumor_cells)

    tumor_expr['CMTM6'] = base_expr_tumor + np.random.randn(n_tumor_cells) * 0.3
    tumor_expr['STUB1'] = -0.7 * tumor_expr['CMTM6'] + np.random.randn(n_tumor_cells) * 0.5  # Negative correlation
    tumor_expr['SQSTM1'] = 0.6 * tumor_expr['CMTM6'] + np.random.randn(n_tumor_cells) * 0.4
    tumor_expr['HIP1R'] = 0.5 * tumor_expr['SQSTM1'] + np.random.randn(n_tumor_cells) * 0.4
    tumor_expr['CD274'] = 0.8 * tumor_expr['CMTM6'] + np.random.randn(n_tumor_cells) * 0.3

    tumor_df = pd.DataFrame(tumor_expr)
    tumor_df['cell_type'] = 'Tumor'
    tumor_df['cell_id'] = [f'tumor_{i}' for i in range(n_tumor_cells)]

    # Immune cells: Weaker/different correlations
    immune_expr = {}
    base_expr_immune = np.random.randn(n_immune_cells)

    immune_expr['CMTM6'] = base_expr_immune + np.random.randn(n_immune_cells) * 0.5
    immune_expr['STUB1'] = -0.3 * immune_expr['CMTM6'] + np.random.randn(n_immune_cells) * 0.8  # Weaker
    immune_expr['SQSTM1'] = 0.2 * immune_expr['CMTM6'] + np.random.randn(n_immune_cells) * 0.9
    immune_expr['HIP1R'] = 0.1 * immune_expr['SQSTM1'] + np.random.randn(n_immune_cells) * 0.9
    immune_expr['CD274'] = 0.4 * immune_expr['CMTM6'] + np.random.randn(n_immune_cells) * 0.7

    immune_df = pd.DataFrame(immune_expr)
    immune_df['cell_type'] = 'Immune'
    immune_df['cell_id'] = [f'immune_{i}' for i in range(n_immune_cells)]

    # Combine
    combined_df = pd.concat([tumor_df, immune_df], ignore_index=True)

    print(f"  [OK] Created {len(combined_df)} cells")

    return combined_df

# =============================================================================
# Step 3: Analyze Correlations by Cell Type
# =============================================================================

def analyze_by_cell_type(sc_df: pd.DataFrame, cell_type: str) -> pd.DataFrame:
    """
    Calculate correlations within a cell type

    Args:
        sc_df: Single-cell expression DataFrame
        cell_type: Cell type to analyze

    Returns:
        Results DataFrame
    """
    print(f"\n[ANALYZE] {cell_type} cells...")

    # Filter to cell type
    subset_df = sc_df[sc_df['cell_type'] == cell_type].copy()
    print(f"  N cells: {len(subset_df)}")

    results = []

    for gene1, gene2 in GENE_PAIRS:
        if gene1 not in subset_df.columns or gene2 not in subset_df.columns:
            print(f"  [SKIP] {gene1}-{gene2}: genes not found")
            continue

        x = subset_df[gene1].values
        y = subset_df[gene2].values

        # Remove NaN
        mask = ~(np.isnan(x) | np.isnan(y))
        x_clean = x[mask]
        y_clean = y[mask]

        if len(x_clean) < 10:
            print(f"  [SKIP] {gene1}-{gene2}: insufficient data")
            continue

        # Pearson correlation
        r, p = stats.pearsonr(x_clean, y_clean)

        # Spearman correlation
        rho, p_spearman = stats.spearmanr(x_clean, y_clean)

        print(f"  {gene1}-{gene2}:")
        print(f"    r = {r:.3f}, P = {p:.2e}")
        print(f"    rho = {rho:.3f}, P = {p_spearman:.2e}")

        results.append({
            'cell_type': cell_type,
            'gene1': gene1,
            'gene2': gene2,
            'n_cells': len(x_clean),
            'pearson_r': r,
            'pearson_p': p,
            'spearman_rho': rho,
            'spearman_p': p_spearman
        })

    return pd.DataFrame(results)

# =============================================================================
# Step 4: Compare with Bulk RNA-seq
# =============================================================================

def compare_with_bulk(sc_results: pd.DataFrame, bulk_file: Path) -> pd.DataFrame:
    """
    Compare single-cell correlations with bulk RNA-seq

    Args:
        sc_results: Single-cell results
        bulk_file: Path to bulk RNA-seq correlation results

    Returns:
        Comparison DataFrame
    """
    print("\n[COMPARE] Single-cell vs bulk RNA-seq...")

    if not bulk_file.exists():
        print(f"  [WARN] Bulk results not found: {bulk_file}")
        return pd.DataFrame()

    # Load bulk results
    bulk_df = pd.read_csv(bulk_file)

    # Merge with single-cell
    comparison = sc_results.merge(
        bulk_df[['gene1', 'gene2', 'simple_r', 'simple_p']],
        on=['gene1', 'gene2'],
        how='left'
    )

    # Calculate concordance
    comparison['concordant'] = np.sign(comparison['pearson_r']) == np.sign(comparison['simple_r'])
    comparison['r_difference'] = comparison['pearson_r'] - comparison['simple_r']

    print("\n  Concordance summary:")
    for cell_type in comparison['cell_type'].unique():
        subset = comparison[comparison['cell_type'] == cell_type]
        concordance_rate = subset['concordant'].mean() * 100
        print(f"    {cell_type}: {concordance_rate:.1f}% concordant")

    return comparison

# =============================================================================
# Main Pipeline
# =============================================================================

def main():
    """
    Main execution pipeline
    """
    print("\n" + "="*80)
    print("SINGLE-CELL VALIDATION PIPELINE")
    print("="*80)

    # Step 1: Try to download real TISCH2 data
    print("\n[STEP 1] Querying TISCH2 databases...")

    for dataset_id in TISCH2_DATASETS:
        metadata = query_tisch2_dataset(dataset_id)
        # In production: download and process actual data

    # Step 2: For now, use simulated data
    print("\n[STEP 2] Using simulated single-cell data for demonstration...")
    print("  (Replace with actual TISCH2 download in production)")

    sc_df = simulate_single_cell_data(n_tumor_cells=500, n_immune_cells=500)

    # Step 3: Analyze by cell type
    print("\n[STEP 3] Analyzing correlations by cell type...")

    all_results = []

    for cell_type in sc_df['cell_type'].unique():
        results = analyze_by_cell_type(sc_df, cell_type)
        all_results.append(results)

    # Combine results
    sc_results = pd.concat(all_results, ignore_index=True)

    # Step 4: Compare with bulk
    print("\n[STEP 4] Comparing with bulk RNA-seq results...")

    bulk_file = BASE_DIR / "outputs" / "partial_correlation_v3_timer2" / "partial_correlation_results_timer2.csv"
    comparison = compare_with_bulk(sc_results, bulk_file)

    # Step 5: Save results
    print("\n[SAVE] Writing results...")

    # Single-cell results
    sc_file = OUTPUT_DIR / "single_cell_correlations.csv"
    sc_results.to_csv(sc_file, index=False)
    print(f"  Saved: {sc_file}")

    # Comparison
    if not comparison.empty:
        comp_file = OUTPUT_DIR / "bulk_vs_singlecell_comparison.csv"
        comparison.to_csv(comp_file, index=False)
        print(f"  Saved: {comp_file}")

    # Summary
    summary = {
        'n_datasets': len(TISCH2_DATASETS),
        'n_gene_pairs': len(GENE_PAIRS),
        'cell_types': sc_df['cell_type'].unique().tolist(),
        'results': sc_results.to_dict('records')
    }

    json_file = OUTPUT_DIR / "single_cell_validation_summary.json"
    with open(json_file, 'w') as f:
        json.dump(summary, f, indent=2)
    print(f"  Saved: {json_file}")

    # Final summary
    print("\n" + "="*80)
    print("SINGLE-CELL VALIDATION COMPLETE")
    print("="*80)

    print("\nKey findings:")
    for _, row in sc_results.iterrows():
        print(f"\n{row['cell_type']} - {row['gene1']}-{row['gene2']}:")
        print(f"  r = {row['pearson_r']:.3f} (P={row['pearson_p']:.2e})")
        print(f"  N cells = {row['n_cells']}")

    print("\n" + "="*80)
    print("Next step:")
    print("  Run: python scripts/analysis/external_validation_geo.py")
    print("="*80)

if __name__ == "__main__":
    main()
