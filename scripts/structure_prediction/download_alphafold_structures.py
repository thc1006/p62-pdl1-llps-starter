#!/usr/bin/env python3
"""
Download AlphaFold structures for key proteins
AlphaFold DB: https://alphafold.ebi.ac.uk/
"""

import requests
from pathlib import Path
import time

# Target proteins with UniProt IDs
PROTEINS = {
    "p62_SQSTM1": "Q13501",    # p62/SQSTM1 - full length
    "PD-L1_CD274": "Q9NZQ7",   # PD-L1/CD274
    "HIP1R": "O75146",         # HIP1R
    "CMTM6": "Q9Y6B0",         # CMTM6
    "STUB1_CHIP": "Q9UNE7",    # STUB1/CHIP
}

def download_alphafold_structure(uniprot_id, output_dir):
    """Download AlphaFold structure for a UniProt ID"""

    # AlphaFold DB URL format - try v4, fallback to v3, v2
    base_url = "https://alphafold.ebi.ac.uk/files"

    # Use latest version (v6 as of 2025-08)
    pdb_url = f"{base_url}/AF-{uniprot_id}-F1-model_v6.pdb"
    output_path = output_dir / f"AF-{uniprot_id}-F1-model_v6.pdb"

    print(f"Downloading {uniprot_id}...")
    print(f"  URL: {pdb_url}")

    try:
        response = requests.get(pdb_url, timeout=30)
        response.raise_for_status()

        with open(output_path, 'wb') as f:
            f.write(response.content)

        # Get file size
        size_mb = output_path.stat().st_size / 1024 / 1024
        print(f"  [OK] Downloaded: {output_path.name} ({size_mb:.2f} MB)")

        # Parse pLDDT scores (in B-factor column)
        plddt_scores = []
        with open(output_path) as f:
            for line in f:
                if line.startswith('ATOM'):
                    plddt = float(line[60:66].strip())
                    plddt_scores.append(plddt)

        if plddt_scores:
            avg_plddt = sum(plddt_scores) / len(plddt_scores)
            print(f"  Average pLDDT: {avg_plddt:.1f} (confidence score)")

            # pLDDT interpretation
            if avg_plddt > 90:
                confidence = "Very high"
            elif avg_plddt > 70:
                confidence = "High"
            elif avg_plddt > 50:
                confidence = "Medium (some disordered regions)"
            else:
                confidence = "Low (mostly disordered)"

            print(f"  Confidence: {confidence}")

        return output_path

    except requests.exceptions.RequestException as e:
        print(f"  [FAIL] Download failed: {e}")
        return None

def main():
    # Create output directory
    output_dir = Path("data/alphafold_structures")
    output_dir.mkdir(parents=True, exist_ok=True)

    print("="*60)
    print("AlphaFold Structure Download")
    print("="*60)
    print(f"Output: {output_dir}\n")

    downloaded = []

    for protein_name, uniprot_id in PROTEINS.items():
        print(f"\n[{protein_name}] UniProt: {uniprot_id}")

        pdb_path = download_alphafold_structure(uniprot_id, output_dir)

        if pdb_path:
            downloaded.append({
                "protein": protein_name,
                "uniprot": uniprot_id,
                "path": str(pdb_path)
            })

        time.sleep(1)  # Be polite to EBI servers

    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    print(f"Downloaded: {len(downloaded)}/{len(PROTEINS)} structures")

    for item in downloaded:
        print(f"  [OK] {item['protein']:15s} ({item['uniprot']})")

    # Save manifest
    import json
    manifest_path = output_dir / "structures_manifest.json"
    with open(manifest_path, 'w') as f:
        json.dump(downloaded, f, indent=2)

    print(f"\nManifest saved: {manifest_path}")
    print("\n🎉 AlphaFold structures ready for Foldseek encoding!")

if __name__ == "__main__":
    main()
