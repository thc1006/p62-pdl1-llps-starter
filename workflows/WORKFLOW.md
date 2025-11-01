# WORKFLOW (v2)

## 0) Bootstrap
```
python -m venv .venv && . .venv/bin/activate && pip install -r requirements.txt
claude
/help
```

## 1) Literature triage
```
/triage "((PD-L1 OR CD274) AND (ubiquitin* OR E3 OR DUB OR deubiquitin*) AND (CMTM6 OR CMTM4 OR HIP1R OR STUB1 OR SPOP OR FBXO22)) :: (NSCLC OR lung cancer)"
```

## 2) TCGA LUAD/LUSC
```
/tcga-run "genes=SQSTM1,CD274,HIP1R,CMTM6,STUB1 cohorts=LUAD,LUSC"
```

## 3) Mutations/CNA (cBioPortal)
```
claude -p "python scripts/cbioportal_genomics.py --config data/cbioportal_profiles.yaml --genes SQSTM1 CD274 HIP1R CMTM6 STUB1 --out outputs/cbioportal"
```

## 4) Structure / LLPS checks
```
/afm-predict "targets=PD-L1_tail|STUB1_TPR|SQSTM1_UBA mode=pairwise"
/llps-scan "proteins=SQSTM1,CD274"
```

## 5) Slides / Preprint
```
/figs2slides "assemble latest figures"
/preprint "refresh paper/preprint_outline.md"
```
