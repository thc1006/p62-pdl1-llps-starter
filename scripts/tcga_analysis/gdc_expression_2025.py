#!/usr/bin/env python3
"""
Fetch TCGA expression data via GDC API (2025-compatible)
Uses STAR-based FPKM from Data Release 41+
"""
import requests
import json
import pandas as pd
import argparse
import os
from pathlib import Path

GDC_API = "https://api.gdc.cancer.gov"

def query_gdc_files(project_ids, data_type="Gene Expression Quantification",
                    workflow="STAR - Counts"):
    """Query GDC for STAR-based gene expression files"""
    filters = {
        "op": "and",
        "content": [
            {"op": "in", "content": {"field": "cases.project.project_id", "value": project_ids}},
            {"op": "=", "content": {"field": "data_type", "value": data_type}},
            {"op": "=", "content": {"field": "analysis.workflow_type", "value": workflow}},
            {"op": "=", "content": {"field": "data_format", "value": "TSV"}}
        ]
    }

    params = {
        "filters": json.dumps(filters),
        "fields": "file_id,file_name,cases.project.project_id,cases.submitter_id,cases.samples.sample_type",
        "format": "JSON",
        "size": 10000
    }

    response = requests.post(f"{GDC_API}/files", json=params)
    response.raise_for_status()
    return response.json()

def download_expression_file(file_id, output_dir):
    """Download a single file from GDC"""
    url = f"{GDC_API}/data/{file_id}"
    response = requests.get(url, stream=True)
    response.raise_for_status()

    filename = f"{file_id}.tsv.gz"
    filepath = output_dir / filename

    with open(filepath, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)

    return filepath

def parse_star_counts(filepath):
    """Parse STAR counts file to extract gene symbols and FPKM"""
    df = pd.read_csv(filepath, sep='\t', compression='infer', comment='#')

    # STAR files have columns: gene_id, gene_name, gene_type, unstranded, stranded_first, stranded_second, tpm_unstranded, fpkm_unstranded, fpkm_uq_unstranded
    # We want gene_name (symbol) and fpkm_unstranded

    if 'fpkm_unstranded' in df.columns:
        result = df[['gene_name', 'fpkm_unstranded']].copy()
        result.columns = ['gene', 'fpkm']
    elif 'tpm_unstranded' in df.columns:
        # Fallback to TPM if FPKM not available
        result = df[['gene_name', 'tpm_unstranded']].copy()
        result.columns = ['gene', 'tpm']
    else:
        raise ValueError(f"No FPKM or TPM column found in {filepath}")

    return result

def main():
    parser = argparse.ArgumentParser(description="Fetch TCGA expression via GDC API (2025)")
    parser.add_argument("--projects", nargs="+", default=["TCGA-LUAD", "TCGA-LUSC"],
                        help="TCGA project IDs")
    parser.add_argument("--genes", nargs="+", default=["SQSTM1", "CD274", "HIP1R", "CMTM6", "STUB1"],
                        help="Gene symbols to extract")
    parser.add_argument("--out", default="outputs/gdc_expression", help="Output directory")
    parser.add_argument("--max_samples", type=int, default=50,
                        help="Max samples per project (for quick test)")
    args = parser.parse_args()

    output_dir = Path(args.out)
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"[GDC] Querying files for projects: {args.projects}")
    result = query_gdc_files(args.projects)

    files = result['data']['hits']
    print(f"[GDC] Found {len(files)} files")

    # Filter for Primary Tumor samples only
    primary_files = []
    for f in files:
        samples = f.get('cases', [{}])[0].get('samples', [])
        if any('Primary Tumor' in s.get('sample_type', '') for s in samples):
            primary_files.append(f)

    print(f"[GDC] Primary Tumor samples: {len(primary_files)}")

    # Limit to max_samples per project for quick testing
    limited_files = primary_files[:args.max_samples]
    print(f"[GDC] Processing {len(limited_files)} samples (limited for speed)")

    # Download and parse files
    expression_data = []

    for i, file_info in enumerate(limited_files, 1):
        file_id = file_info['file_id']
        case_id = file_info['cases'][0]['submitter_id']
        project_id = file_info['cases'][0]['project']['project_id']

        print(f"[{i}/{len(limited_files)}] Downloading {case_id} ({project_id})...")

        try:
            filepath = download_expression_file(file_id, output_dir)
            expr = parse_star_counts(filepath)

            # Filter to genes of interest
            expr_filtered = expr[expr['gene'].isin(args.genes)]

            # Add metadata
            expr_filtered['case_id'] = case_id
            expr_filtered['project'] = project_id

            expression_data.append(expr_filtered)

            # Clean up downloaded file to save space
            os.remove(filepath)

        except Exception as e:
            print(f"  ERROR: {e}")
            continue

    # Combine all data
    if expression_data:
        combined = pd.concat(expression_data, ignore_index=True)

        # Pivot to wide format: rows=samples, cols=genes
        wide = combined.pivot_table(
            index=['case_id', 'project'],
            columns='gene',
            values='fpkm' if 'fpkm' in combined.columns else 'tpm'
        ).reset_index()

        # Save
        output_file = output_dir / "expression_matrix.csv"
        wide.to_csv(output_file, index=False)
        print(f"\n[GDC] Saved expression matrix: {output_file}")
        print(f"[GDC] Shape: {wide.shape}")
        print(f"\n[GDC] Sample preview:")
        print(wide.head())

        return output_file
    else:
        print("[GDC] No data retrieved!")
        return None

if __name__ == "__main__":
    main()
