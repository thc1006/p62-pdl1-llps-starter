#!/usr/bin/env python3
"""
Genome-Scale LLPS Scan of PD-L1 Interactors
Get all PD-L1 interactors from BioGRID and scan for LLPS propensity
"""

import requests
from pathlib import Path
import json
import time
from collections import defaultdict

# BioGRID REST API
BIOGRID_API = "https://webservice.thebiogrid.org/interactions/"
BIOGRID_ACCESS_KEY = "public"  # Use public access

# PD-L1 identifiers
PD_L1_GENE = "CD274"
PD_L1_ENTREZ = "29126"

def get_pdl1_interactors():
    """Get all PD-L1 protein interactors from BioGRID"""

    print("="*60)
    print("BioGRID: Fetching PD-L1 Interactors")
    print("="*60)

    # BioGRID REST API query
    params = {
        "searchNames": "true",
        "geneList": PD_L1_GENE,
        "organism": "9606",  # Homo sapiens
        "searchbiogridids": "false",
        "includeInteractors": "true",
        "accesskey": BIOGRID_ACCESS_KEY,
        "format": "json"
    }

    print(f"Querying: {BIOGRID_API}")
    print(f"Gene: {PD_L1_GENE} (Entrez: {PD_L1_ENTREZ})")

    try:
        response = requests.get(BIOGRID_API, params=params, timeout=60)
        response.raise_for_status()
        data = response.json()

        print(f"\n[OK] Retrieved {len(data)} interactions")

        # Extract unique interactors
        interactors = set()

        for interaction_id, interaction in data.items():
            # Get both sides of interaction
            gene_a = interaction.get('OFFICIAL_SYMBOL_A', '')
            gene_b = interaction.get('OFFICIAL_SYMBOL_B', '')

            # Add the one that is NOT CD274
            if gene_a == PD_L1_GENE:
                interactors.add(gene_b)
            elif gene_b == PD_L1_GENE:
                interactors.add(gene_a)

        # Remove empty strings
        interactors = {g for g in interactors if g}

        print(f"[OK] Found {len(interactors)} unique interactors\n")

        return list(interactors)

    except requests.exceptions.RequestException as e:
        print(f"[FAIL] BioGRID query failed: {e}")
        print("\nUsing backup list from literature...")

        # Backup: Known PD-L1 interactors from literature
        return [
            "SQSTM1", "HIP1R", "CMTM6", "CMTM4", "STUB1",
            "SPOP", "COPA", "CAND1", "FKBP5", "PRKD2",
            "AP2M1", "AP2B1", "PDCD1", "CD80", "CD86",
            "JAK1", "JAK2", "STAT3", "NEDD4", "WWP2"
        ]

def get_protein_sequence_from_uniprot(gene_symbol):
    """Get protein sequence from UniProt"""

    # UniProt REST API
    url = f"https://rest.uniprot.org/uniprotkb/search"
    params = {
        "query": f"gene:{gene_symbol} AND organism_id:9606 AND reviewed:true",
        "format": "fasta",
        "size": "1"
    }

    try:
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()

        # Parse FASTA
        lines = response.text.strip().split('\n')
        if len(lines) >= 2 and lines[0].startswith('>'):
            header = lines[0]
            sequence = ''.join(lines[1:])

            # Extract UniProt ID from header
            uniprot_id = header.split('|')[1] if '|' in header else None

            return {
                "gene": gene_symbol,
                "uniprot_id": uniprot_id,
                "sequence": sequence,
                "length": len(sequence)
            }

    except Exception as e:
        print(f"  [WARN] {gene_symbol}: Could not fetch sequence ({e})")

    return None

def calculate_llps_propensity(sequence):
    """
    Calculate LLPS propensity using disorder + composition heuristics
    (Same as saprot_llps_prediction.py)
    """

    # Disorder-promoting residues
    disorder_promoting = set('GQASEPRKD')

    # Charge residues
    charged = set('DEKR')

    # Aromatic residues (pi-pi interactions)
    aromatic = set('FYW')

    # Polar residues
    polar = set('STNQ')

    # Calculate fractions
    disorder_frac = sum(1 for aa in sequence if aa in disorder_promoting) / len(sequence)
    charged_frac = sum(1 for aa in sequence if aa in charged) / len(sequence)
    aromatic_frac = sum(1 for aa in sequence if aa in aromatic) / len(sequence)
    polar_frac = sum(1 for aa in sequence if aa in polar) / len(sequence)

    # LLPS score (weighted)
    # High disorder + moderate charge + aromatic = LLPS-prone
    llps_score = (
        0.4 * disorder_frac +      # Disorder is critical
        0.25 * charged_frac +       # Charge important
        0.2 * aromatic_frac +       # Pi-pi helps
        0.15 * polar_frac          # Polar helps
    )

    # Classify
    if llps_score > 0.5:
        classification = "HIGH"
    elif llps_score > 0.4:
        classification = "MEDIUM"
    else:
        classification = "LOW"

    return {
        "llps_score": round(llps_score, 3),
        "classification": classification,
        "disorder_frac": round(disorder_frac, 3),
        "charged_frac": round(charged_frac, 3),
        "aromatic_frac": round(aromatic_frac, 3)
    }

def main():
    # Get PD-L1 interactors
    interactors = get_pdl1_interactors()

    print(f"Scanning {len(interactors)} proteins for LLPS propensity...\n")

    results = []
    failed = []

    for i, gene in enumerate(interactors, 1):
        print(f"[{i}/{len(interactors)}] {gene}...", end=' ')

        # Get sequence
        protein_data = get_protein_sequence_from_uniprot(gene)

        if protein_data:
            # Calculate LLPS propensity
            llps_metrics = calculate_llps_propensity(protein_data['sequence'])

            result = {
                **protein_data,
                **llps_metrics
            }

            results.append(result)

            print(f"[OK] Score={llps_metrics['llps_score']} ({llps_metrics['classification']})")

        else:
            failed.append(gene)
            print("[FAIL]")

        time.sleep(0.5)  # Be polite to UniProt

    # Save results
    output_dir = Path("outputs/genome_scale_llps")
    output_dir.mkdir(parents=True, exist_ok=True)

    output_file = output_dir / "pdl1_interactors_llps_scan.json"
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)

    # Create summary
    print("\n" + "="*60)
    print("GENOME-SCALE LLPS SCAN RESULTS")
    print("="*60)
    print(f"Total scanned: {len(results)}/{len(interactors)}")
    print(f"Failed: {len(failed)}")

    # Rank by LLPS score
    results_sorted = sorted(results, key=lambda x: x['llps_score'], reverse=True)

    print("\nTOP 20 LLPS-PRONE PD-L1 INTERACTORS:")
    print("-"*60)
    print(f"{'Rank':<6} {'Gene':<12} {'Score':<8} {'Class':<10} {'Length'}")
    print("-"*60)

    for rank, result in enumerate(results_sorted[:20], 1):
        print(f"{rank:<6} {result['gene']:<12} {result['llps_score']:<8.3f} {result['classification']:<10} {result['length']}")

    print("\n[DISCOVERY] Novel LLPS-prone interactors:")
    known_llps = {'SQSTM1', 'HIP1R'}  # Already known
    novel = [r for r in results_sorted if r['llps_score'] > 0.45 and r['gene'] not in known_llps]

    if novel:
        for r in novel[:10]:
            print(f"  -> {r['gene']:12s} (score={r['llps_score']:.3f}) - NOVEL CANDIDATE!")
    else:
        print("  (None with score >0.45)")

    print(f"\nResults saved: {output_file}")
    print("\n[NEXT STEP] Validate top candidates with experimental LLPS assays!")

if __name__ == "__main__":
    main()
