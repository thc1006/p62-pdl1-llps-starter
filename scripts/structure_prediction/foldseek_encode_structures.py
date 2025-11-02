#!/usr/bin/env python3
"""
Encode AlphaFold structures using Foldseek (3Di alphabet)
Required for structure-aware SaProt inference
"""

import subprocess
from pathlib import Path
import json

# Paths
FOLDSEEK_BIN = "tools/foldseek/foldseek/bin/foldseek"
STRUCTURE_DIR = Path("data/alphafold_structures")
OUTPUT_DIR = Path("data/foldseek_encoded")

def run_foldseek_struct2seq(pdb_file, output_prefix):
    """
    Run Foldseek struct2seq to get 3Di encoding

    Foldseek converts 3D structures to a sequence-like representation
    using the 3Di alphabet (structural alphabet with 20 characters)
    """

    cmd = [
        FOLDSEEK_BIN,
        "structureto3didescriptor",
        str(pdb_file),
        str(output_prefix)
    ]

    print(f"Running: {' '.join(cmd)}")

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=60
        )

        if result.returncode == 0:
            print(f"  [OK] Success")
            return True
        else:
            print(f"  [FAIL] Error: {result.stderr}")
            return False

    except FileNotFoundError:
        print(f"  [FAIL] Foldseek not found at: {FOLDSEEK_BIN}")
        print(f"  Attempting to use WSL...")

        # Try via WSL
        wsl_cmd = ["wsl", FOLDSEEK_BIN, "structureto3didescriptor",
                   str(pdb_file).replace('\\', '/'),
                   str(output_prefix).replace('\\', '/')]

        result = subprocess.run(wsl_cmd, capture_output=True, text=True, timeout=60)

        if result.returncode == 0:
            print(f"  [OK] Success via WSL")
            return True
        else:
            print(f"  [FAIL] WSL also failed: {result.stderr}")
            return False

    except Exception as e:
        print(f"  [FAIL] Exception: {e}")
        return False

def parse_3di_output(output_file):
    """Parse Foldseek 3Di output"""
    try:
        with open(output_file) as f:
            lines = f.readlines()

        # Foldseek output format: FASTA-like
        sequences = {}
        current_id = None
        current_seq = []

        for line in lines:
            line = line.strip()
            if line.startswith('>'):
                if current_id:
                    sequences[current_id] = ''.join(current_seq)
                current_id = line[1:].split()[0]
                current_seq = []
            else:
                current_seq.append(line)

        if current_id:
            sequences[current_id] = ''.join(current_seq)

        return sequences

    except Exception as e:
        print(f"  [FAIL] Could not parse output: {e}")
        return None

def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    print("="*60)
    print("Foldseek 3Di Encoding")
    print("="*60)
    print(f"Input: {STRUCTURE_DIR}")
    print(f"Output: {OUTPUT_DIR}\n")

    # Load structure manifest
    manifest_file = STRUCTURE_DIR / "structures_manifest.json"
    with open(manifest_file) as f:
        structures = json.load(f)

    encoded = []

    for struct in structures:
        protein = struct['protein']
        uniprot = struct['uniprot']
        pdb_path = Path(struct['path'])

        print(f"\n[{protein}] {uniprot}")
        print(f"  PDB: {pdb_path.name}")

        # Output files
        output_prefix = OUTPUT_DIR / f"{uniprot}_3di"

        # Run Foldseek
        success = run_foldseek_struct2seq(pdb_path, output_prefix)

        if success:
            # Parse output
            output_file = Path(str(output_prefix) + ".tsv")

            if output_file.exists():
                sequences = parse_3di_output(output_file)

                if sequences:
                    for seq_id, seq in sequences.items():
                        print(f"  3Di sequence ({len(seq)} residues): {seq[:60]}...")

                        encoded.append({
                            "protein": protein,
                            "uniprot": uniprot,
                            "3di_sequence": seq,
                            "length": len(seq)
                        })
                else:
                    print(f"  [WARN] Could not parse 3Di output")
            else:
                print(f"  [WARN] Output file not found: {output_file}")

    # Save encoded sequences
    if encoded:
        output_json = OUTPUT_DIR / "encoded_3di_sequences.json"
        with open(output_json, 'w') as f:
            json.dump(encoded, f, indent=2)

        print("\n" + "="*60)
        print("SUMMARY")
        print("="*60)
        print(f"Encoded: {len(encoded)} structures")
        print(f"Saved to: {output_json}")

        for item in encoded:
            print(f"  [OK] {item['protein']:15s} ({item['length']} residues)")

        print("\n[NEXT STEP] Use these 3Di sequences for SaProt structure-aware inference!")

    else:
        print("\n[FAIL] No structures encoded successfully")
        print("\nAlternative: Use simplified approach without Foldseek")
        print("  - Download pre-computed ESM embeddings")
        print("  - Or use sequence-only SaProt (already done)")

if __name__ == "__main__":
    main()
