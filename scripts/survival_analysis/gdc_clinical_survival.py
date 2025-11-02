#!/usr/bin/env python3
"""
GDC clinical survival extractor (LUAD/LUSC).
Refs:
- GDC API search & retrieval: https://docs.gdc.cancer.gov/API/Users_Guide/Search_and_Retrieval/
"""
import argparse, os, json, requests, pandas as pd

API = "https://api.gdc.cancer.gov"

def gdc_cases(project):
    filters = {"op":"in","content":{"field":"project.project_id","value":[f"TCGA-{project}"]}}
    fields = [
        "case_id","submitter_id","project.project_id",
        "diagnoses.vital_status","diagnoses.days_to_death","diagnoses.days_to_last_follow_up",
        "demographic.gender","demographic.age_at_index"
    ]
    params = {
        "filters": json.dumps(filters),
        "fields": ",".join(fields),
        "format": "JSON",
        "size": "10000"
    }
    r = requests.get(f"{API}/cases", params=params, timeout=120)
    r.raise_for_status()
    hits = r.json()["data"]["hits"]
    rows = []
    for h in hits:
        diag = (h.get("diagnoses") or [{}])[0]
        rows.append({
            "case_id": h.get("case_id"),
            "patient": h.get("submitter_id"),
            "project": (h.get("project") or {}).get("project_id"),
            "vital_status": (diag or {}).get("vital_status"),
            "days_to_death": (diag or {}).get("days_to_death"),
            "days_to_last_follow_up": (diag or {}).get("days_to_last_follow_up"),
            "gender": (h.get("demographic") or {}).get("gender"),
            "age_at_index": (h.get("demographic") or {}).get("age_at_index")
        })
    return pd.DataFrame(rows)

def compute_survival(df):
    import numpy as np
    d_death = pd.to_numeric(df["days_to_death"], errors="coerce")
    d_fu = pd.to_numeric(df["days_to_last_follow_up"], errors="coerce")
    os_time = d_death.fillna(d_fu)
    os_event = (~d_death.isna()).astype(int)
    out = df.copy()
    out["OS_time"] = os_time
    out["OS_event"] = os_event
    return out

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cohorts", nargs="+", default=["LUAD","LUSC"])
    ap.add_argument("--out", default="outputs/tcga")
    args = ap.parse_args()
    os.makedirs(args.out, exist_ok=True)
    frames = []
    for c in args.cohorts:
        df = gdc_cases(c)
        df["cohort"] = c
        frames.append(df)
    big = pd.concat(frames, ignore_index=True)
    sur = compute_survival(big)
    outp = os.path.join(args.out, "clinical_survival.csv")
    sur.to_csv(outp, index=False)
    print("Saved", outp)

if __name__ == "__main__":
    main()
