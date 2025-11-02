#!/usr/bin/env python3
"""
Process TCGA RNA-seq Expression Data
Combines individual HTSeq count files into expression matrix

Input: Raw TCGA HTSeq files
Output: Normalized expression matrix (samples x genes)

Author: Automated Pipeline
Date: 2025-11-02
"""

import os
import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, List
import re

# =============================================================================
# Configuration
# =============================================================================

BASE_DIR = Path(__file__).parent.parent.parent
DATA_DIR = BASE_DIR / "data" / "tcga_raw"
OUTPUT_DIR = BASE_DIR / "outputs" / "tcga_full_cohort_real"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

PROJECTS = ['TCGA-LUAD', 'TCGA-LUSC', 'TCGA-SKCM']

# =============================================================================
# Step 1: Read Individual HTSeq Files
# =============================================================================

def read_htseq_file(file_path: Path) -> pd.Series:
    """
    Read single HTSeq count file

    Format:
    ENSG00000000003.15    1234
    ENSG00000000005.6     56
    ...

    Args:
        file_path: Path to HTSeq file

    Returns:
        Series with gene IDs as index, counts as values
    """
    df = pd.read_csv(file_path, sep='\t', header=None,
                    names=['gene_id', 'count'], index_col=0)

    # Remove summary statistics lines
    df = df[~df.index.str.startswith('__')]

    # Extract Ensembl ID without version
    df.index = df.index.str.split('.').str[0]

    return df['count']

def process_project_expression(project_id: str) -> pd.DataFrame:
    """
    Process all HTSeq files for a project

    Args:
        project_id: TCGA project ID (e.g., 'TCGA-LUAD')

    Returns:
        Expression DataFrame (genes x samples)
    """
    project_dir = DATA_DIR / project_id
    print(f"\n[PROCESS] {project_id}")

    if not project_dir.exists():
        print(f"  [ERROR] Directory not found: {project_dir}")
        return pd.DataFrame()

    # Find all HTSeq files
    htseq_files = list(project_dir.glob("**/*htseq.counts.gz")) + \
                  list(project_dir.glob("**/*htseq.counts")) + \
                  list(project_dir.glob("**/*.tsv"))

    if not htseq_files:
        print(f"  [WARN] No HTSeq files found in {project_dir}")
        return pd.DataFrame()

    print(f"  Found {len(htseq_files)} files")

    # Read all files
    expression_dict = {}

    for i, file_path in enumerate(htseq_files, 1):
        if i % 50 == 0:
            print(f"  Processing: {i}/{len(htseq_files)}")

        try:
            # Extract sample ID from file path
            # Usually in format: /path/to/TCGA-XX-XXXX-XXA/file.tsv
            sample_id = file_path.parent.name

            counts = read_htseq_file(file_path)
            expression_dict[sample_id] = counts

        except Exception as e:
            print(f"  [ERROR] Failed to read {file_path.name}: {e}")
            continue

    # Combine into DataFrame
    expr_df = pd.DataFrame(expression_dict)
    print(f"  Created matrix: {expr_df.shape[0]} genes x {expr_df.shape[1]} samples")

    return expr_df

# =============================================================================
# Step 2: Gene ID Conversion (Ensembl to Symbol)
# =============================================================================

def get_gene_symbol_mapping() -> Dict[str, str]:
    """
    Download Ensembl to Gene Symbol mapping

    Uses Ensembl BioMart or local annotation file

    Returns:
        Dict mapping Ensembl ID to gene symbol
    """
    print("\n[MAPPING] Getting Ensembl to Gene Symbol mapping...")

    # Try to download from GENCODE
    try:
        import requests

        url = "https://ftp.ebi.ac.uk/pub/databases/gencode/Gencode_human/release_44/gencode.v44.annotation.gtf.gz"
        print(f"  Downloading from GENCODE...")

        # This is large (~50MB), consider using cached version
        mapping_file = DATA_DIR / "gencode_v44_mapping.txt"

        if mapping_file.exists():
            print(f"  Using cached mapping: {mapping_file}")
            mapping_df = pd.read_csv(mapping_file, sep='\t')
        else:
            print(f"  [WARN] Mapping file not found")
            print(f"  Using gene IDs as-is")
            return {}

        # Parse GTF to extract gene_id and gene_name
        mapping = dict(zip(mapping_df['gene_id'], mapping_df['gene_name']))
        print(f"  Loaded {len(mapping)} gene mappings")

        return mapping

    except Exception as e:
        print(f"  [ERROR] Failed to get mapping: {e}")
        return {}

def convert_gene_ids(expr_df: pd.DataFrame, mapping: Dict[str, str]) -> pd.DataFrame:
    """
    Convert Ensembl IDs to gene symbols

    Args:
        expr_df: Expression DataFrame with Ensembl IDs
        mapping: Ensembl to symbol mapping

    Returns:
        Expression DataFrame with gene symbols
    """
    print("\n[CONVERT] Converting Ensembl IDs to gene symbols...")

    if not mapping:
        print("  [SKIP] No mapping available, keeping Ensembl IDs")
        return expr_df

    # Map IDs
    expr_df.index = expr_df.index.map(lambda x: mapping.get(x, x))

    # Remove genes without symbols (still Ensembl IDs)
    has_symbol = ~expr_df.index.str.startswith('ENSG')
    expr_df = expr_df[has_symbol]

    # Handle duplicate symbols (keep first)
    expr_df = expr_df[~expr_df.index.duplicated(keep='first')]

    print(f"  Final: {expr_df.shape[0]} genes with symbols")

    return expr_df

# =============================================================================
# Step 3: Normalization
# =============================================================================

def normalize_expression(expr_df: pd.DataFrame, method='tpm') -> pd.DataFrame:
    """
    Normalize expression counts

    Args:
        expr_df: Raw count matrix
        method: 'tpm' or 'fpkm' or 'log2tpm'

    Returns:
        Normalized expression DataFrame
    """
    print(f"\n[NORMALIZE] Normalizing expression ({method})...")

    # Filter low-expression genes
    # Keep genes expressed (count >= 1) in at least 10% of samples
    min_samples = int(expr_df.shape[1] * 0.1)
    expressed = (expr_df >= 1).sum(axis=1) >= min_samples
    expr_df = expr_df[expressed]
    print(f"  Filtered to {expr_df.shape[0]} expressed genes")

    if method == 'tpm':
        # TPM normalization (if gene lengths available, simplified here)
        # TPM = (count / length) * 1e6 / sum(count / length)

        # Without gene lengths, use total count normalization
        total_counts = expr_df.sum(axis=0)
        expr_df = expr_df / total_counts * 1e6

    elif method == 'log2tpm':
        # Log2(TPM + 1)
        total_counts = expr_df.sum(axis=0)
        expr_df = expr_df / total_counts * 1e6
        expr_df = np.log2(expr_df + 1)

    print(f"  Range: {expr_df.min().min():.2f} to {expr_df.max().max():.2f}")

    return expr_df

def zscore_normalize(expr_df: pd.DataFrame) -> pd.DataFrame:
    """
    Z-score normalization (per gene)

    Args:
        expr_df: Expression DataFrame

    Returns:
        Z-score normalized DataFrame
    """
    print("\n[Z-SCORE] Normalizing by gene...")

    expr_z = expr_df.T  # Transpose for zscore (works on columns)
    expr_z = (expr_z - expr_z.mean()) / expr_z.std()
    expr_z = expr_z.T

    print(f"  Mean: {expr_z.mean().mean():.2f}, Std: {expr_z.std().mean():.2f}")

    return expr_z

# =============================================================================
# Step 4: Quality Control
# =============================================================================

def quality_control(expr_df: pd.DataFrame, project_id: str) -> pd.DataFrame:
    """
    Perform quality control

    Args:
        expr_df: Expression DataFrame
        project_id: Project ID

    Returns:
        QC-passed DataFrame
    """
    print(f"\n[QC] Quality control for {project_id}...")

    initial_samples = expr_df.shape[1]
    initial_genes = expr_df.shape[0]

    # 1. Remove samples with too many zeros
    zero_fraction = (expr_df == 0).sum(axis=0) / expr_df.shape[0]
    good_samples = zero_fraction < 0.5
    expr_df = expr_df.loc[:, good_samples]
    print(f"  Samples: {initial_samples} -> {expr_df.shape[1]} "
          f"(removed {initial_samples - expr_df.shape[1]} low-quality)")

    # 2. Remove genes with zero variance
    gene_var = expr_df.var(axis=1)
    good_genes = gene_var > 0
    expr_df = expr_df[good_genes]
    print(f"  Genes: {initial_genes} -> {expr_df.shape[0]} "
          f"(removed {initial_genes - expr_df.shape[0]} zero-variance)")

    # 3. Check for outliers (optional)
    # Use PCA or other methods

    return expr_df

# =============================================================================
# Main Pipeline
# =============================================================================

def main():
    """
    Main execution pipeline
    """
    print("\n" + "="*80)
    print("TCGA EXPRESSION DATA PROCESSING PIPELINE")
    print("="*80)

    # Step 1: Get gene mapping
    gene_mapping = get_gene_symbol_mapping()

    # Step 2: Process each project
    all_projects_data = {}

    for project_id in PROJECTS:
        # Read raw counts
        expr_df = process_project_expression(project_id)

        if expr_df.empty:
            continue

        # Convert IDs
        expr_df = convert_gene_ids(expr_df, gene_mapping)

        # Normalize
        expr_df = normalize_expression(expr_df, method='log2tpm')

        # QC
        expr_df = quality_control(expr_df, project_id)

        # Z-score
        expr_df = zscore_normalize(expr_df)

        all_projects_data[project_id] = expr_df

    # Step 3: Combine all projects
    print("\n[COMBINE] Merging all projects...")

    # Find common genes
    common_genes = set(all_projects_data[PROJECTS[0]].index)
    for project_id in PROJECTS[1:]:
        if project_id in all_projects_data:
            common_genes &= set(all_projects_data[project_id].index)

    print(f"  Common genes: {len(common_genes)}")

    # Merge
    combined_dfs = []
    for project_id, expr_df in all_projects_data.items():
        # Keep only common genes
        expr_df = expr_df.loc[list(common_genes)]

        # Add cancer type column
        samples = expr_df.columns.tolist()
        expr_df = expr_df.T
        expr_df['cancer_type'] = project_id.replace('TCGA-', '')
        expr_df['sample_id'] = samples

        combined_dfs.append(expr_df)

    # Concatenate
    final_df = pd.concat(combined_dfs, axis=0, ignore_index=False)

    print(f"\n[FINAL] Combined matrix: {final_df.shape[0]} samples x {final_df.shape[1]} variables")

    # Step 4: Save
    output_file = OUTPUT_DIR / "expression_matrix_full_real.csv"
    final_df.to_csv(output_file, index=False)
    print(f"\n[SAVED] {output_file}")

    # Summary statistics
    print("\n" + "="*80)
    print("SUMMARY")
    print("="*80)
    for cancer_type in final_df['cancer_type'].unique():
        count = (final_df['cancer_type'] == cancer_type).sum()
        print(f"  {cancer_type}: {count} samples")
    print(f"  Total: {final_df.shape[0]} samples")
    print(f"  Genes: {final_df.shape[1] - 2} genes")  # Exclude cancer_type, sample_id
    print("="*80)

    print("\nNext step:")
    print("  Run: python scripts/data_pipeline/03_process_clinical.py")

if __name__ == "__main__":
    main()
