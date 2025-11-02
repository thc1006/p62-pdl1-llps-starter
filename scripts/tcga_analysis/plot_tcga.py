#!/usr/bin/env python3
"""Produce simple placeholder figures from TCGA outputs."""
import argparse, os, pandas as pd
import matplotlib.pyplot as plt

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="indir", default="outputs/tcga")
    ap.add_argument("--figdir", default="figures/tcga")
    args = ap.parse_args()
    os.makedirs(args.figdir, exist_ok=True)
    inp = os.path.join(args.indir,"mock_survival_input.csv")
    if not os.path.exists(inp):
        print("No mock data; run tcga_survival.py first.")
        return
    df = pd.read_csv(inp)
    for cohort, g in df.groupby("cohort"):
        ax = g["CD274"].hist(bins=30)
        ax.set_title(f"CD274 distribution — {cohort}")
        out = os.path.join(args.figdir, f"cd274_hist_{cohort}.png")
        plt.savefig(out, dpi=160)
        plt.close('all')
        print("Saved", out)

if __name__ == "__main__":
    main()
