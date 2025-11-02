#!/usr/bin/env python3
"""Fetch selected gene expression or alteration data from cBioPortal REST API
and save as CSV. See https://docs.cbioportal.org/web-api-and-clients/
"""
import argparse, requests, pandas as pd, sys, os

API = os.environ.get("CBIO_API", "https://www.cbioportal.org/api")

def get_molecular_profiles(study_id):
    url = f"{API}/molecular-profiles"
    params = {"studyId": study_id}
    r = requests.get(url, params=params, headers={"accept":"application/json"})
    r.raise_for_status()
    return r.json()

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--study", default="nsclc_tcga_broad_2016", help="cBioPortal study ID")
    ap.add_argument("--out", default="outputs/cbioportal")
    args = ap.parse_args()
    os.makedirs(args.out, exist_ok=True)
    profiles = get_molecular_profiles(args.study)
    import pandas as pd
    pd.DataFrame(profiles).to_csv(os.path.join(args.out,"profiles.csv"), index=False)
    with open(os.path.join(args.out,"README.txt"),"w") as f:
        f.write("Fetched profiles list. Extend script to pull profile data per gene/sample.\n")
    print("Done. Profiles listing saved.", file=sys.stderr)

if __name__ == "__main__":
    main()
