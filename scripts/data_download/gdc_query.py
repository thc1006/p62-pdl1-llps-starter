#!/usr/bin/env python3
"""Minimal GDC API query to fetch case/clinical metadata for cohorts and save as CSV.
Docs: https://gdc.cancer.gov/developers/gdc-application-programming-interface-api
"""
import argparse, requests, os, pandas as pd, sys, json

API = "https://api.gdc.cancer.gov"

def cases(project_code):
    url = f"{API}/cases"
    filters = {
        "op": "in",
        "content": {"field": "project.project_id", "value": [f"TCGA-{project_code}"]}
    }
    params = {
        "filters": json.dumps(filters),
        "size": "10000"
    }
    r = requests.get(url, params=params)
    r.raise_for_status()
    hits = r.json().get("data", {}).get("hits", [])
    return pd.json_normalize(hits)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cohorts", nargs="+", default=["LUAD","LUSC"])
    ap.add_argument("--out", default="outputs/tcga")
    args = ap.parse_args()
    os.makedirs(args.out, exist_ok=True)
    frames = []
    for cohort in args.cohorts:
        try:
            df = cases(cohort)
            df["cohort"] = cohort
            frames.append(df)
        except Exception as e:
            print(f"[warn] {cohort}: {e}", file=sys.stderr)
    if frames:
        out = os.path.join(args.out,"clinical_cases.csv")
        pd.concat(frames, ignore_index=True).to_csv(out, index=False)
        print("Saved", out)
    else:
        print("No data.", file=sys.stderr)

if __name__ == "__main__":
    main()
