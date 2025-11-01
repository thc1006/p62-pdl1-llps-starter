setup:
	python -m venv .venv && . .venv/bin/activate && pip install -r requirements.txt

triage:
	claude -p "/triage (PD-L1 ubiquitin E3 DUB CMTM6 CMTM4 HIP1R STUB1 SPOP FBXO22) :: (NSCLC OR lung cancer)"

tcga:
	claude -p "/tcga-run genes=SQSTM1,CD274,HIP1R,CMTM6,STUB1 cohorts=LUAD,LUSC"

cbioportal:
	python scripts/cbioportal_genomics.py --config data/cbioportal_profiles.yaml --genes SQSTM1 CD274 HIP1R CMTM6 STUB1 --out outputs/cbioportal

preprint:
	claude -p "/preprint"
