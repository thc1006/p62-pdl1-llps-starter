#!/usr/bin/env python3
"""
Complete TCGA Data Download Pipeline
Downloads full RNA-seq and clinical data for LUAD, LUSC, SKCM

Requirements:
- gdc-client (https://gdc.cancer.gov/access-data/gdc-data-transfer-tool)
- requests, pandas

Author: Automated Pipeline
Date: 2025-11-02
"""

import os
import sys
import json
import requests
import pandas as pd
import subprocess
from pathlib import Path
from typing import List, Dict
import time

# =============================================================================
# Configuration
# =============================================================================

BASE_DIR = Path(__file__).parent.parent.parent
DATA_DIR = BASE_DIR / "data" / "tcga_raw"
OUTPUT_DIR = BASE_DIR / "outputs" / "tcga_full_cohort_real"

# Create directories
DATA_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# TCGA projects
PROJECTS = {
    'TCGA-LUAD': 'Lung Adenocarcinoma',
    'TCGA-LUSC': 'Lung Squamous Cell Carcinoma',
    'TCGA-SKCM': 'Skin Cutaneous Melanoma'
}

# GDC API endpoints
GDC_API = "https://api.gdc.cancer.gov"
FILES_ENDPOINT = f"{GDC_API}/files"
CASES_ENDPOINT = f"{GDC_API}/cases"

# =============================================================================
# Step 1: Query GDC for Files
# =============================================================================

def query_gdc_files(project_id: str, data_category: str, data_type: str) -> List[str]:
    """
    Query GDC API for file UUIDs

    Args:
        project_id: TCGA project ID (e.g., 'TCGA-LUAD')
        data_category: 'Transcriptome Profiling' or 'Clinical'
        data_type: 'Gene Expression Quantification' or 'Clinical Supplement'

    Returns:
        List of file UUIDs
    """
    print(f"\n[QUERY] {project_id} - {data_category}")

    filters = {
        "op": "and",
        "content": [
            {"op": "in", "content": {"field": "cases.project.project_id", "value": [project_id]}},
            {"op": "in", "content": {"field": "files.data_category", "value": [data_category]}},
            {"op": "in", "content": {"field": "files.data_type", "value": [data_type]}}
        ]
    }

    if data_category == 'Transcriptome Profiling':
        # Add workflow filter for RNA-seq
        filters["content"].append({
            "op": "in",
            "content": {
                "field": "files.analysis.workflow_type",
                "value": ["STAR - Counts"]
            }
        })

    params = {
        "filters": json.dumps(filters),
        "fields": "file_id,file_name,cases.submitter_id,file_size",
        "format": "JSON",
        "size": "10000"  # Max results
    }

    response = requests.get(FILES_ENDPOINT, params=params)
    response.raise_for_status()

    data = response.json()
    hits = data["data"]["hits"]

    file_ids = [hit["file_id"] for hit in hits]
    total_size_gb = sum(hit["file_size"] for hit in hits) / (1024**3)

    print(f"  Found {len(file_ids)} files ({total_size_gb:.2f} GB)")

    return file_ids

# =============================================================================
# Step 2: Download Files Using GDC Client
# =============================================================================

def download_with_gdc_client(file_ids: List[str], output_dir: Path) -> bool:
    """
    Download files using gdc-client

    Args:
        file_ids: List of file UUIDs
        output_dir: Output directory

    Returns:
        Success status
    """
    # Create output directory
    output_dir.mkdir(parents=True, exist_ok=True)

    # Create manifest file
    manifest_path = output_dir / "gdc_manifest.txt"

    with open(manifest_path, 'w') as f:
        f.write("id\n")
        for file_id in file_ids:
            f.write(f"{file_id}\n")

    print(f"\n[DOWNLOAD] Starting download of {len(file_ids)} files...")
    print(f"  Manifest: {manifest_path}")
    print(f"  Output: {output_dir}")

    # Check if gdc-client is installed
    try:
        subprocess.run(["gdc-client", "--version"],
                      check=True,
                      capture_output=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("\n[ERROR] gdc-client not found!")
        print("Please install from: https://gdc.cancer.gov/access-data/gdc-data-transfer-tool")
        print("\nWindows installation:")
        print("  1. Download gdc-client.exe")
        print("  2. Add to PATH or place in project directory")
        return False

    # Download
    cmd = [
        "gdc-client", "download",
        "-m", str(manifest_path),
        "-d", str(output_dir),
        "--n-processes", "8",  # Parallel downloads
        "--retry-amount", "3"
    ]

    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print(result.stdout)
        print("\n[SUCCESS] Download completed!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n[ERROR] Download failed: {e}")
        print(e.stderr)
        return False

# =============================================================================
# Step 3: Alternative - Direct HTTP Download (No GDC Client Needed)
# =============================================================================

def download_file_direct(file_id: str, output_path: Path) -> bool:
    """
    Download single file via HTTP (fallback method)

    Args:
        file_id: File UUID
        output_path: Output file path

    Returns:
        Success status
    """
    url = f"https://api.gdc.cancer.gov/data/{file_id}"

    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()

        with open(output_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        return True
    except Exception as e:
        print(f"  [ERROR] Failed to download {file_id}: {e}")
        return False

def download_all_direct(file_ids: List[str], output_dir: Path,
                       project_id: str) -> bool:
    """
    Download all files via direct HTTP

    Args:
        file_ids: List of file UUIDs
        output_dir: Output directory
        project_id: Project ID for subfolder

    Returns:
        Success status
    """
    project_dir = output_dir / project_id
    project_dir.mkdir(parents=True, exist_ok=True)

    print(f"\n[DOWNLOAD] Starting direct HTTP download of {len(file_ids)} files...")

    success_count = 0
    for i, file_id in enumerate(file_ids, 1):
        print(f"  [{i}/{len(file_ids)}] Downloading {file_id}...", end='')

        output_file = project_dir / f"{file_id}.tsv"

        if output_file.exists():
            print(" [SKIP] Already exists")
            success_count += 1
            continue

        if download_file_direct(file_id, output_file):
            print(" [OK]")
            success_count += 1
        else:
            print(" [FAIL]")

        # Rate limiting
        time.sleep(0.5)

    print(f"\n[COMPLETE] Downloaded {success_count}/{len(file_ids)} files")
    return success_count == len(file_ids)

# =============================================================================
# Step 4: Download Clinical Data
# =============================================================================

def download_clinical_data(project_id: str, output_dir: Path) -> bool:
    """
    Download clinical data using GDC API

    Args:
        project_id: TCGA project ID
        output_dir: Output directory

    Returns:
        Success status
    """
    print(f"\n[CLINICAL] Downloading clinical data for {project_id}...")

    # Query for clinical files
    filters = {
        "op": "and",
        "content": [
            {"op": "in", "content": {"field": "cases.project.project_id", "value": [project_id]}},
            {"op": "in", "content": {"field": "files.data_category", "value": ["Clinical"]}}
        ]
    }

    params = {
        "filters": json.dumps(filters),
        "fields": "file_id,file_name",
        "format": "JSON",
        "size": "10000"
    }

    response = requests.get(FILES_ENDPOINT, params=params)
    data = response.json()

    clinical_files = data["data"]["hits"]
    print(f"  Found {len(clinical_files)} clinical files")

    # Download each file
    clinical_dir = output_dir / f"{project_id}_clinical"
    clinical_dir.mkdir(parents=True, exist_ok=True)

    for i, file_info in enumerate(clinical_files, 1):
        file_id = file_info["file_id"]
        file_name = file_info["file_name"]

        print(f"  [{i}/{len(clinical_files)}] {file_name}...", end='')

        output_path = clinical_dir / file_name

        if output_path.exists():
            print(" [SKIP]")
            continue

        if download_file_direct(file_id, output_path):
            print(" [OK]")
        else:
            print(" [FAIL]")

    return True

# =============================================================================
# Step 5: Query Summary
# =============================================================================

def query_all_projects():
    """
    Query all projects and show data availability
    """
    print("\n" + "="*80)
    print("TCGA DATA AVAILABILITY SUMMARY")
    print("="*80)

    for project_id, project_name in PROJECTS.items():
        print(f"\n{project_id}: {project_name}")
        print("-" * 40)

        # RNA-seq
        rna_files = query_gdc_files(
            project_id,
            "Transcriptome Profiling",
            "Gene Expression Quantification"
        )

        # Clinical
        clinical_files = query_gdc_files(
            project_id,
            "Clinical",
            "Clinical Supplement"
        )

        print(f"\n  RNA-seq files: {len(rna_files)}")
        print(f"  Clinical files: {len(clinical_files)}")

    print("\n" + "="*80)

# =============================================================================
# Main Pipeline
# =============================================================================

def main():
    """
    Main execution pipeline
    """
    print("\n" + "="*80)
    print("TCGA COMPLETE DATA DOWNLOAD PIPELINE")
    print("="*80)

    # Step 1: Query data availability
    print("\n[STEP 1] Querying GDC for available data...")
    query_all_projects()

    # Check for auto-execution mode
    auto_mode = '--auto' in sys.argv or '--auto-download' in sys.argv or os.environ.get('AUTO_DOWNLOAD', '').lower() in ['1', 'true', 'yes']

    # Ask user for download method
    print("\n[STEP 2] Choose download method:")
    print("  1. GDC Client (faster, recommended)")
    print("  2. Direct HTTP (slower, no install needed)")
    print("  3. Skip download (query only)")

    if auto_mode:
        print("\n[AUTO-MODE] Using GDC Client (option 1)")
        choice = '1'
    else:
        choice = input("\nEnter choice (1/2/3): ").strip()

    if choice == '3':
        print("\n[DONE] Query complete. Download skipped.")
        return

    # Step 2: Download RNA-seq data
    print("\n[STEP 3] Downloading RNA-seq data...")

    for project_id in PROJECTS.keys():
        print(f"\n--- {project_id} ---")

        # Query files
        rna_files = query_gdc_files(
            project_id,
            "Transcriptome Profiling",
            "Gene Expression Quantification"
        )

        if not rna_files:
            print(f"  [WARN] No RNA-seq files found for {project_id}")
            continue

        # Download
        if choice == '1':
            success = download_with_gdc_client(rna_files, DATA_DIR / project_id)
        else:
            success = download_all_direct(rna_files, DATA_DIR, project_id)

        if not success:
            print(f"  [ERROR] Download failed for {project_id}")

    # Step 3: Download clinical data
    print("\n[STEP 4] Downloading clinical data...")

    for project_id in PROJECTS.keys():
        download_clinical_data(project_id, DATA_DIR)

    # Summary
    print("\n" + "="*80)
    print("DOWNLOAD COMPLETE")
    print("="*80)
    print(f"\nData saved to: {DATA_DIR}")
    print("\nNext steps:")
    print("  1. Run: python scripts/data_pipeline/02_process_expression.py")
    print("  2. Run: python scripts/data_pipeline/03_process_clinical.py")
    print("="*80)

if __name__ == "__main__":
    main()
