#!/usr/bin/env python3
"""
Parallel TCGA Download Accelerator
Downloads LUSC and SKCM in parallel with LUAD
"""

import subprocess
import json
import requests
from pathlib import Path

# Config
GDC_API = "https://api.gdc.cancer.gov/files"
DATA_DIR = Path("data/tcga_raw")
DATA_DIR.mkdir(parents=True, exist_ok=True)

def query_and_create_manifest(project_id, data_dir):
    """Query GDC and create manifest for a project"""
    print(f"\n[{project_id}] Querying GDC...")

    filters = {
        "op": "and",
        "content": [
            {"op": "in", "content": {"field": "cases.project.project_id", "value": [project_id]}},
            {"op": "in", "content": {"field": "files.data_category", "value": ["Transcriptome Profiling"]}},
            {"op": "in", "content": {"field": "files.data_type", "value": ["Gene Expression Quantification"]}},
            {"op": "in", "content": {"field": "files.analysis.workflow_type", "value": ["STAR - Counts"]}}
        ]
    }

    params = {
        "filters": json.dumps(filters),
        "fields": "file_id,file_name,file_size",
        "format": "JSON",
        "size": "10000"
    }

    response = requests.get(GDC_API, params=params)
    response.raise_for_status()

    hits = response.json()["data"]["hits"]
    file_ids = [hit["file_id"] for hit in hits]
    total_gb = sum(hit["file_size"] for hit in hits) / (1024**3)

    print(f"[{project_id}] Found {len(file_ids)} files ({total_gb:.2f} GB)")

    # Create manifest
    project_dir = data_dir / project_id
    project_dir.mkdir(parents=True, exist_ok=True)

    manifest_path = project_dir / "gdc_manifest.txt"
    with open(manifest_path, 'w') as f:
        f.write("id\n")
        for fid in file_ids:
            f.write(f"{fid}\n")

    print(f"[{project_id}] Manifest created: {manifest_path}")
    return manifest_path, project_dir

def start_download(project_id, manifest_path, output_dir):
    """Start gdc-client download in background"""
    cmd = [
        "gdc-client", "download",
        "-m", str(manifest_path),
        "-d", str(output_dir),
        "--n-processes", "8",
        "--retry-amount", "3"
    ]

    log_file = output_dir / f"download_{project_id}.log"

    print(f"[{project_id}] Starting download...")
    print(f"[{project_id}] Log: {log_file}")

    with open(log_file, 'w') as f:
        process = subprocess.Popen(
            cmd,
            stdout=f,
            stderr=subprocess.STDOUT,
            cwd=Path.cwd()
        )

    print(f"[{project_id}] Download started (PID: {process.pid})")
    return process

if __name__ == "__main__":
    projects = ["TCGA-LUSC", "TCGA-SKCM"]

    print("="*60)
    print("PARALLEL TCGA DOWNLOAD ACCELERATOR")
    print("="*60)

    processes = []

    for project in projects:
        try:
            manifest, output_dir = query_and_create_manifest(project, DATA_DIR)
            proc = start_download(project, manifest, output_dir)
            processes.append((project, proc))
        except Exception as e:
            print(f"[{project}] ERROR: {e}")

    print("\n" + "="*60)
    print(f"Started {len(processes)} parallel downloads!")
    print("="*60)
    print("\nMonitor with:")
    for project, proc in processes:
        print(f"  tail -f data/tcga_raw/{project}/download_{project}.log")
    print("\nOr use: bash monitor_progress.sh")
