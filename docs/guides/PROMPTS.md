# Claude Code Prompts (copy-paste ready)

> Use these inside **Claude Code** (CLI/Console/Web). They assume this repo root as the working directory.

---

## Phase 0 — Bootstrap

### P0.S1 — Initialize project & tools
```
You are my DevOps assistant. 
Tasks:
1) Create a Python venv and install requirements.txt 
2) Show me how to start an interactive `claude` session and list Slash Commands.
Constraints: Do not change repo layout. Output exact shell lines only.

Deliverables:
- commands to run venv and `pip install -r requirements.txt`
- a one-liner to start `claude`
- how to call `/help` and list `.claude/commands`
```

### P0.S2 — Configure MCP servers
```
Open `mcp/servers.json` and ensure servers for filesystem, git, http-cbioportal, http-gdc, http-depmap are present.
If missing, add them. Then explain how to run `/mcp` to verify connections.
```

---

## Phase 1 — Literature Evidence Map (E-utilities)

### P1.S1 — Implement PubMed triage (E-utilities)
```
Goal: Implement scripts/pubmed_triage.py to query PubMed (ESearch→ESummary/EFetch) for the last 8 years,
deduplicate, and write:
- outputs/evidence/evidence_table.csv (PMID, DOI, Year, Journal, System, Assay, Manipulation, Key Proteins, Finding, Strength)
- outputs/evidence/bib.bib

Spec:
- Input: --query '((PD-L1 OR CD274) AND (ubiquitin* OR E3 OR DUB OR deubiquitin*) AND (CMTM6 OR CMTM4 OR HIP1R OR STUB1 OR SPOP OR FBXO22))'
- Date: --mindate 2017 --maxdate 3000
- Rate-limit: polite (append tool+email), support API key via env ENTrez_API_KEY
- Extract DOI from ESummary (ArticleIds) or PubMed XML
- BibTeX: minimal @article with title, authors, journal, year, volume, pages, doi, pmid

File to modify/create:
- scripts/pubmed_triage.py
- .claude/commands/triage.md should route to `python scripts/pubmed_triage.py` with args
```

### P1.S2 — Auto-annotate LLPS rigor fields
```
Extend scripts/pubmed_triage.py:
- Pattern-match FRAP/1,6-hexanediol/condensate keywords to fill 'LLPS_methods' and 'Rigor_flags' columns.
- Update evidence_table.csv and summary.md accordingly.
```

---

## Phase 2 — TCGA (LUAD/LUSC) Expression + Survival

### P2.S1 — Fetch expression matrices via UCSC Xena
```
Implement scripts/xena_tcga_expression.py:
- Download TCGA LUAD and LUSC gene expression matrices (e.g., HTSeq FPKM or TPM) from UCSC Xena public hub.
- Accept flags: --cohorts LUAD LUSC --genes SQSTM1 CD274 HIP1R CMTM6 STUB1 --out outputs/xena
- Save per-cohort gene×sample CSV and a joined long-table.
Notes:
- Use the Xena dataset index JSON to resolve dataset URLs when possible; otherwise document fallback URLs inside code comments.
```

### P2.S2 — Pull clinical/survival from GDC and compute OS
```
Implement scripts/gdc_clinical_survival.py:
- Query GDC /cases with filters project_id in [TCGA-LUAD, TCGA-LUSC]
- Extract per patient: vital_status, days_to_death, days_to_last_follow_up
- Compute OS_time (days) and OS_event (1=dead,0=censored)
- Map case IDs to sample barcodes
- Output: outputs/tcga/clinical_survival.csv
```

### P2.S3 — Join expression + survival and run analyses
```
Implement scripts/tcga_join_and_analyze.py:
- Merge Xena expression with GDC survival by patient/sample mapping
- For each gene: median-split → KM plots; Cox PH with age/sex if available
- Save: figures/tcga/KM_*.png, outputs/tcga/stats/*.csv, outputs/tcga/summary.md
- Use lifelines; ensure reproducibility (seeded)
```

### P2.S4 — Add mutations & CNA via cBioPortal
```
Implement scripts/cbioportal_genomics.py:
- Given study_ids for LUAD/LUSC and molecular_profile_ids for mrna/mutation/cna,
  fetch: mutation status (binary per gene), GISTIC discrete CNA, and mRNA z-scores if available.
- Merge with expression/survival table; produce simple box/violin plots of expression by mutation/CNA status.
- Provide REST fallback if pybioportal is unavailable.

Configs:
- data/cbioportal_profiles.yaml → study, sample_list_id, molecular_profile_ids
```

---

## Phase 3 — Structure/LLPS Checks

### P3.S1 — Domain FASTA builder
```
Create scripts/domains_fasta.py:
- Build FASTA files for human PD-L1 cytosolic tail, STUB1 TPR, SQSTM1 UBA/PB1
- Write to data/fasta/*.fa with UniProt IDs in headers
```

### P3.S2 — AF-Multimer plan
```
Update .claude/commands/afm-predict.md:
- Add instructions for conda install of colabfold and a small GPU sanity run
- Ensure outputs are stored in outputs/afm and figures/structure
```

---

## Phase 4 — Artifacts & Packaging

### P4.S1 — Assemble figures → slides
```
Make /figs2slides compose artifacts/slides/p62-pdl1-llps-slides.pptx and .pdf
Use captions from outputs/**/summary.md
```

### P4.S2 — Preprint compile
```
Run /preprint to refresh paper/preprint_outline.md and export PDF to artifacts/preprint/paper.pdf
```
