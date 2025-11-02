#!/usr/bin/env python3
"""
Download Mega TCGA Cohort (n=1000+)
===================================
Automated download of large-scale TCGA expression data for Nature-level analysis

Features:
- Parallel downloads (10 concurrent threads)
- Progress tracking
- Auto-retry on failure
- Support for multiple cancer types

Target cohorts:
- TCGA-LUAD: 500 samples (lung adenocarcinoma)
- TCGA-LUSC: 300 samples (lung squamous)
- TCGA-SKCM: 200 samples (melanoma - high PD-L1)
Total: 1000 samples

Author: Enhancement Pipeline
Date: 2025-11-02
"""

import requests
import json
import time
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime

class TCGAMegaDownloader:
    """High-performance TCGA data downloader"""

    def __init__(self, output_dir="outputs/gdc_expression", max_workers=10):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        self.max_workers = max_workers
        self.genes = ['SQSTM1', 'CD274', 'HIP1R', 'CMTM6', 'STUB1']

        self.gdc_api = "https://api.gdc.cancer.gov"
        self.stats = {
            "total": 0,
            "downloaded": 0,
            "failed": 0,
            "skipped": 0
        }

    def query_files(self, project, max_files=500):
        """Query GDC for STAR gene expression files"""
        print(f"\n🔍 Querying GDC for {project}...")

        filters = {
            "op": "and",
            "content": [
                {"op": "in", "content": {"field": "cases.project.project_id", "value": [project]}},
                {"op": "in", "content": {"field": "files.data_type", "value": ["Gene Expression Quantification"]}},
                {"op": "in", "content": {"field": "files.analysis.workflow_type", "value": ["STAR - Counts"]}}
            ]
        }

        params = {
            "filters": json.dumps(filters),
            "fields": "file_id,file_name,file_size",
            "format": "json",
            "size": max_files
        }

        try:
            response = requests.post(
                f"{self.gdc_api}/files",
                json=params,
                timeout=30
            )
            response.raise_for_status()

            data = response.json()
            hits = data['data']['hits']

            print(f"✅ Found {len(hits)} files for {project}")
            return hits

        except Exception as e:
            print(f"❌ Query failed: {e}")
            return []

    def download_file(self, file_info, retry=3):
        """Download a single file with retry logic"""
        file_id = file_info['file_id']
        file_name = file_info['file_name']
        output_path = self.output_dir / file_name

        # Skip if already exists
        if output_path.exists():
            self.stats["skipped"] += 1
            return {"status": "skipped", "file": file_name}

        # Download with retry
        for attempt in range(retry):
            try:
                response = requests.get(
                    f"{self.gdc_api}/data/{file_id}",
                    timeout=120
                )
                response.raise_for_status()

                # Save file
                output_path.write_bytes(response.content)

                self.stats["downloaded"] += 1
                return {"status": "success", "file": file_name}

            except Exception as e:
                if attempt == retry - 1:
                    self.stats["failed"] += 1
                    return {"status": "failed", "file": file_name, "error": str(e)}
                time.sleep(2 ** attempt)  # Exponential backoff

    def download_cohort(self, project, max_files=500):
        """Download entire cohort with parallel downloads"""
        print(f"\n{'='*60}")
        print(f"DOWNLOADING: {project}")
        print(f"Target: {max_files} samples")
        print(f"{'='*60}\n")

        # Query files
        files = self.query_files(project, max_files)
        if not files:
            print(f"⚠️  No files found for {project}")
            return

        self.stats["total"] += len(files)

        # Download in parallel
        print(f"📥 Downloading {len(files)} files ({self.max_workers} workers)...")
        start_time = time.time()

        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = {executor.submit(self.download_file, f): f for f in files}

            completed = 0
            for future in as_completed(futures):
                result = future.result()
                completed += 1

                if completed % 50 == 0 or completed == len(files):
                    elapsed = time.time() - start_time
                    rate = completed / elapsed if elapsed > 0 else 0
                    print(f"  Progress: {completed}/{len(files)} ({rate:.1f} files/sec)")

        elapsed = time.time() - start_time
        print(f"\n✅ {project} download complete ({elapsed:.1f}s)")

    def run_mega_download(self):
        """Execute full mega cohort download"""
        print("="*60)
        print("🚀 MEGA TCGA COHORT DOWNLOAD")
        print("="*60)
        print(f"Start time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Output directory: {self.output_dir}")
        print(f"Target genes: {', '.join(self.genes)}")
        print()

        start_time = time.time()

        # Download each cohort
        cohorts = [
            ("TCGA-LUAD", 500),  # Lung adenocarcinoma
            ("TCGA-LUSC", 300),  # Lung squamous
            ("TCGA-SKCM", 200)   # Melanoma
        ]

        for project, max_files in cohorts:
            self.download_cohort(project, max_files)

        # Final statistics
        elapsed = time.time() - start_time
        print("\n" + "="*60)
        print("📊 DOWNLOAD STATISTICS")
        print("="*60)
        print(f"Total files queried: {self.stats['total']}")
        print(f"Successfully downloaded: {self.stats['downloaded']}")
        print(f"Skipped (already exist): {self.stats['skipped']}")
        print(f"Failed: {self.stats['failed']}")
        print(f"Total time: {elapsed/3600:.2f} hours")
        print(f"Average rate: {self.stats['downloaded']/elapsed:.2f} files/sec")
        print("="*60)

        # Save stats
        stats_file = self.output_dir / "download_stats.json"
        with open(stats_file, 'w') as f:
            json.dump({
                **self.stats,
                "duration_seconds": elapsed,
                "timestamp": datetime.now().isoformat()
            }, f, indent=2)

        print(f"\n✅ Statistics saved: {stats_file}")

def main():
    """Main execution"""
    downloader = TCGAMegaDownloader(
        output_dir="outputs/gdc_expression",
        max_workers=10  # Parallel downloads
    )

    downloader.run_mega_download()

if __name__ == "__main__":
    main()
