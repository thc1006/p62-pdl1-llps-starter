# Skill: TCGA LUAD/LUSC pipeline

## Purpose
Fetch expression/clinical data via GDC and cBioPortal; compute correlations, survival curves, and immune infiltration proxies; produce figures.

## Inputs
- Gene list (e.g., SQSTM1, CD274, HIP1R, CMTM6, STUB1).

## Outputs
- `outputs/tcga/*.csv`, `figures/tcga/*`, `outputs/tcga/summary.md`.

## Steps
1) GDC: query and download expression + clinical for LUAD/LUSC.
2) Correlation (Pearson/Spearman), KM survival (median split), Cox multivariate.
3) Optional: immune infiltration scores (ESTIMATE‑like proxy if no deconvolution available).
