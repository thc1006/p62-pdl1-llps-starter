#!/usr/bin/env python3
"""
Join Xena expression and GDC survival → KM plots & Cox PH.
"""
import argparse, os, pandas as pd, numpy as np
import matplotlib.pyplot as plt
from lifelines import KaplanMeierFitter, CoxPHFitter

def map_sample_to_patient(sample_id):
    parts = sample_id.split("-")
    if len(parts) >= 3:
        return "-".join(parts[:3])
    return sample_id

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--expr", required=True)
    ap.add_argument("--clinical", required=True)
    ap.add_argument("--out", default="outputs/tcga")
    ap.add_argument("--figdir", default="figures/tcga")
    ap.add_argument("--genes", nargs="+", default=["SQSTM1","CD274","HIP1R","CMTM6","STUB1"])
    args = ap.parse_args()
    os.makedirs(args.out, exist_ok=True)
    os.makedirs(args.figdir, exist_ok=True)

    expr = pd.read_csv(args.expr)
    expr["patient"] = expr["sample"].apply(map_sample_to_patient)
    clin = pd.read_csv(args.clinical)

    merged = expr.merge(clin, left_on=["patient","cohort"], right_on=["patient","cohort"], how="inner")

    summaries = []
    for g in args.genes:
        sub = merged[merged["gene"].str.contains(g)]
        if sub.empty:
            continue
        for cohort, grp in sub.groupby("cohort"):
            df = grp.copy()
            med = df["expr"].median()
            df["high"] = (df["expr"] >= med).astype(int)

            km = KaplanMeierFitter()
            plt.figure()
            for label, gg in df.groupby("high"):
                km.fit(durations=gg["OS_time"], event_observed=gg["OS_event"], label=("High" if label==1 else "Low"))
                km.plot_survival_function()
            plt.title(f"{g} median split — {cohort}")
            plt.xlabel("Days"); plt.ylabel("Survival probability")
            km_path = os.path.join(args.figdir, f"KM_{g}_{cohort}.png")
            plt.savefig(km_path, dpi=160); plt.close('all')

            cdf = df[["OS_time","OS_event","expr"]].dropna()
            if len(cdf) > 10:
                cph = CoxPHFitter()
                cph.fit(cdf, duration_col="OS_time", event_col="OS_event")
                hr = float(np.exp(cph.params_["expr"]))
                p = float(cph.summary.loc["expr","p"])
            else:
                hr, p = float("nan"), float("nan")

            summaries.append({"gene":g,"cohort":cohort,"median":med,"KM_fig":km_path,"HR_expr":hr,"P_expr":p,"n":len(df)})

    outcsv = os.path.join(args.out,"summary_stats.csv")
    pd.DataFrame(summaries).to_csv(outcsv, index=False)
    with open(os.path.join(args.out,"summary.md"),"w") as f:
        f.write("# TCGA analysis summary\n\n")
        for s in summaries:
            f.write(f"- {s['gene']} {s['cohort']}: HR={s['HR_expr']:.3g}, p={s['P_expr']:.3g}, n={s['n']}, fig={s['KM_fig']}\n")
    print("Saved", outcsv)

if __name__ == "__main__":
    main()
