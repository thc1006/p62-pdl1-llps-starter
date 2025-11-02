#!/usr/bin/env python3
"""
Prepare sequences for AlphaFold-Multimer prediction
"""
from pathlib import Path

def prepare_sequences():
    """Create FASTA files for p62-PD-L1 complex prediction"""

    # p62 PB1 domain (residues 1-120)
    p62_pb1_seq = "MADEAGARPGGRRPRGRRLPGPGDPGAGAPRPTPRPPPPGPATAEQEQGPLDSCEEDGEEDEEGGKSVEQEPEESEEDEDDDDFEDDDEWED"

    # PD-L1 cytoplasmic tail (residues 239-290)
    pdl1_cyto_seq = "RMKQVEHKIKGSQEQGKGRSEQRKMTILHQVKDAGTKIKGTGVHEQGKTHKQIKQRDSQKHQRMTHQKRMTHLK"

    # Create FASTA file
    output_dir = Path("data")
    output_dir.mkdir(parents=True, exist_ok=True)

    fasta_path = output_dir / "p62_pdl1_sequences.fasta"

    with open(fasta_path, 'w') as f:
        f.write(">p62_PB1_domain\n")
        f.write(p62_pb1_seq + "\n")
        f.write(">PD-L1_cytoplasmic_tail\n")
        f.write(pdl1_cyto_seq + "\n")

    print(f"✅ Created: {fasta_path}")
    print(f"   p62 PB1: {len(p62_pb1_seq)} aa")
    print(f"   PD-L1 cyto: {len(pdl1_cyto_seq)} aa")

if __name__ == "__main__":
    prepare_sequences()
