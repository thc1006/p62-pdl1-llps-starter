#!/usr/bin/env python3
"""
Quick analysis using partial downloaded files
"""
import pandas as pd
import glob
from pathlib import Path

# Find all downloaded TSV files
data_dir = Path("outputs/gdc_expression")
files = list(data_dir.glob("*.tsv.gz"))

print(f"Found {len(files)} files")

# Genes of interest
genes_of_interest = ['SQSTM1', 'CD274', 'HIP1R', 'CMTM6', 'STUB1']

# Parse all files
expression_data = []

for i, file_path in enumerate(files, 1):
    print(f"[{i}/{len(files)}] Parsing {file_path.name}")

    # Files are plain text despite .tsv.gz extension - must disable compression
    df = pd.read_csv(file_path, sep='\t', comment='#', compression=None)

    # Extract FPKM
    if 'fpkm_unstranded' in df.columns:
        expr = df[['gene_name', 'fpkm_unstranded']].copy()
        expr.columns = ['gene', 'fpkm']
    else:
        print(f"  Skipping (no FPKM column)")
        continue

    # Filter to genes of interest
    expr_filtered = expr[expr['gene'].isin(genes_of_interest)]
    expr_filtered['sample_id'] = file_path.stem  # Use filename as sample ID

    expression_data.append(expr_filtered)

# Combine
if expression_data:
    combined = pd.concat(expression_data, ignore_index=True)

    # Pivot to wide format
    wide = combined.pivot_table(
        index='sample_id',
        columns='gene',
        values='fpkm'
    ).reset_index()

    print(f"\nExpression matrix shape: {wide.shape}")
    print(f"\nColumns: {wide.columns.tolist()}")
    print(f"\nPreview:")
    print(wide.head())

    # Quick correlation
    if 'SQSTM1' in wide.columns and 'CD274' in wide.columns:
        from scipy import stats

        valid = wide[['SQSTM1', 'CD274']].dropna()
        if len(valid) >= 5:
            r, p = stats.pearsonr(valid['SQSTM1'], valid['CD274'])
            print(f"\n=== PRELIMINARY CORRELATION ===")
            print(f"SQSTM1 vs CD274:")
            print(f"  Pearson r = {r:.3f}")
            print(f"  P-value = {p:.3f}")
            print(f"  n = {len(valid)}")

            if p < 0.1:
                print(f"\n✅ Promising! Continue full analysis")
            else:
                print(f"\n⚠️  Weak signal. May need larger sample or pivot strategy")
else:
    print("No data parsed!")
