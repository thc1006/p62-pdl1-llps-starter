#!/usr/bin/env python3
"""DepMap bulk download helper: guide users to pick files and store locally.
Portal: https://depmap.org/portal/
"""
import argparse, os, textwrap

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="outputs/depmap")
    args = ap.parse_args()
    os.makedirs(args.out, exist_ok=True)
    with open(os.path.join(args.out,"README.txt"),"w") as f:
        f.write(textwrap.dedent("""        Visit the DepMap data portal All Data page to download the latest releases
        (e.g., CCLE_expression.csv, gene_effect.csv). Place them in this folder.
        """))
    print("Placeholder created. See README in outputs/depmap.")

if __name__ == "__main__":
    main()
