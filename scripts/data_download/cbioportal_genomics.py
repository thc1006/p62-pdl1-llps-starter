#!/usr/bin/env python3
"""
Fetch mutations/CNA/mRNA z-scores from cBioPortal and merge for quick plots.

Refs:
- cBioPortal REST API: https://www.cbioportal.org/api/swagger-ui/index.html
- Bioconductor cBioPortalData: https://waldronlab.io/cBioPortalData/reference/cBioPortal.html
- pybioportal docs: https://pybioportal.readthedocs.io/en/stable/molecular_data.html
"""
import argparse, os, yaml, requests, pandas as pd
import matplotlib.pyplot as plt

def get_mol_data(base, molecular_profile_id, sample_list_id, entrez_gene_ids):
    url = f"{base}/molecular-profiles/{molecular_profile_id}/molecular-data/fetch"
    payload = {
        "entrezGeneIds": [int(x) if str(x).isdigit() else x for x in entrez_gene_ids],
        "sampleListId": sample_list_id
    }
    r = requests.post(url, json=payload, timeout=120, headers={"accept":"application/json"})
    r.raise_for_status()
    return pd.DataFrame(r.json())

def get_gene_panel(base, gene_symbols):
    r = requests.post(f"{base}/genes/fetch", json={"geneSymbols": gene_symbols}, timeout=60, headers={"accept":"application/json"})
    if r.status_code == 200:
        df = pd.DataFrame(r.json())
        return dict(zip(df["hugoGeneSymbol"], df["entrezGeneId"]))
    return {s: None for s in gene_symbols}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default="data/cbioportal_profiles.yaml")
    ap.add_argument("--genes", nargs="+", default=["SQSTM1","CD274","HIP1R","CMTM6","STUB1"])
    ap.add_argument("--out", default="outputs/cbioportal")
    args = ap.parse_args()
    os.makedirs(args.out, exist_ok=True)
    cfg = yaml.safe_load(open(args.config))
    base = cfg.get("base_url","https://www.cbioportal.org/api")
    idmap = get_gene_panel(base, args.genes)
    entrez = [v for v in idmap.values() if v is not None]

    for cohort, st in cfg["studies"].items():
        sample_list_id = st["sample_list_id"]
        z = get_mol_data(base, st["mrna_zscore_profile"], sample_list_id, entrez)
        mut = requests.get(f"{base}/studies/{st['study_id']}/mutations?sampleListId={sample_list_id}", timeout=120, headers={"accept":"application/json"})
        mut.raise_for_status()
        mut_df = pd.DataFrame(mut.json())
        cna = get_mol_data(base, st["cna_profile"], sample_list_id, entrez)

        z.to_csv(os.path.join(args.out, f"{cohort}_mrna_z.csv"), index=False)
        mut_df.to_csv(os.path.join(args.out, f"{cohort}_mutations.csv"), index=False)
        cna.to_csv(os.path.join(args.out, f"{cohort}_cna.csv"), index=False)

        try:
            cd274_eid = idmap.get("CD274")
            if cd274_eid is None: continue
            z_cd274 = z[z["entrezGeneId"]==cd274_eid]
            stub1_eid = idmap.get("STUB1")
            if stub1_eid is not None and not mut_df.empty:
                stub1_samples = set(mut_df.loc[mut_df["entrezGeneId"]==stub1_eid, "sampleId"].unique())
                z_cd274 = z_cd274.copy()
                z_cd274["STUB1_mut"] = z_cd274["sampleId"].apply(lambda s: 1 if s in stub1_samples else 0)
                ax = z_cd274.boxplot(column="value", by="STUB1_mut")
                ax.set_title(f"CD274 z-score by STUB1_mut — {cohort}")
                ax.set_xlabel("STUB1_mut (1=yes)")
                figp = os.path.join("figures/cbioportal", f"cd274_by_stub1_{cohort}.png")
                os.makedirs(os.path.dirname(figp), exist_ok=True)
                import matplotlib.pyplot as plt
                plt.suptitle("")
                plt.savefig(figp, dpi=160); plt.close("all")
        except Exception as e:
            print("[warn]", e)

    print("cBioPortal fetch done.")

if __name__ == "__main__":
    main()
