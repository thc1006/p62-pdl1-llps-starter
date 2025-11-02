#!/usr/bin/env python3
"""
Download TCGA LUAD/LUSC gene expression from UCSC Xena.

Refs:
- Xena platform overview: https://xena.ucsc.edu/
- Xena download docs: https://xena.ucsc.edu/download-data
We default to TCGA Pan-Cancer HTSeq FPKM matrix when available.
"""
import argparse, os, io, gzip, requests, pandas as pd

DEFAULT_URL = "https://gdc-hub.s3.us-east-1.amazonaws.com/download/TCGA-PANCAN.htseq_fpkm.tsv.gz"

def fetch(url):
    r = requests.get(url, timeout=120)
    r.raise_for_status()
    return io.BytesIO(r.content)

def subset_matrix(bio, cohorts, genes):
    with gzip.open(bio, "rt", encoding="utf-8", newline="") as f:
        df = pd.read_csv(f, sep="\t", index_col=0)
    keep_cols = [c for c in df.columns if any(("TCGA-"+co) in c for co in cohorts)]
    df = df[keep_cols]
    if genes:
        idx = df.index
        def match(i):
            if "|" in i:
                a,b = i.split("|",1)
                return a in genes or b in genes
            return i in genes
        sel = [i for i in idx if match(i)]
        df = df.loc[sel]
    return df

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--url", default=DEFAULT_URL)
    ap.add_argument("--cohorts", nargs="+", default=["LUAD","LUSC"])
    ap.add_argument("--genes", nargs="+", default=["SQSTM1","CD274","HIP1R","CMTM6","STUB1"])
    ap.add_argument("--out", default="outputs/xena")
    args = ap.parse_args()
    os.makedirs(args.out, exist_ok=True)
    bio = fetch(args.url)
    df = subset_matrix(bio, args.cohorts, set(args.genes))
    long_rows = []
    for cohort in args.cohorts:
        cols = [c for c in df.columns if ("TCGA-"+cohort) in c]
        sub = df[cols]
        sub.to_csv(os.path.join(args.out, f"expr_{cohort}.csv"))
        for g in sub.index:
            for s in cols:
                long_rows.append({"cohort":cohort,"sample":s,"gene":g,"expr":sub.loc[g, s]})
    pd.DataFrame(long_rows).to_csv(os.path.join(args.out, "joined_long.csv"), index=False)
    print("Saved expression tables to", args.out)

if __name__ == "__main__":
    main()
