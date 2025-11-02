# Skill: Literature triage & evidence extraction

## Purpose
Automate PubMed/PMC search→deduplicate→extract→summarize into a structured CSV and BibTeX.

## Inputs
- Query string; optional date range; inclusion/exclusion rules.

## Outputs
- `outputs/evidence/evidence_table.csv`, `outputs/evidence/bib.bib`, `outputs/evidence/summary.md`.

## Guidance
- Prefer 2017–present; prioritize primary data and high‑quality reviews.
- Capture assay types (Co‑IP, FRAP, CHX chase, internalization/recycling) and outcome measures.
- Note LLPS method rigor (FRAP parameters; hexanediol caveats).

## Tooling
- Allowed tools: Bash(curl, jq), Python (requests, pandas).

## Validation
- Spot‑check 3 random entries; verify DOIs; ensure reproducibility of the CSV pipeline.
