# Project: LLPS-related PD-L1 regulatory network paper (TCGA-based)

You are Claude Code, running in a project that contains:
- A computational immuno-oncology manuscript about PD-L1 (CD274) and four regulators
  (CMTM6, STUB1, SQSTM1, HIP1R), framed in the context of LLPS (liquid–liquid phase separation).
- Analysis scripts for TCGA bulk RNA-seq and immune deconvolution.
- This project is currently a **bioRxiv-style preprint** that needs major scientific and writing revisions.

Your primary job in this repo is to:
1. **Audit and repair the scientific design**, especially survival analysis and LLPS framing.
2. **Rewrite and reorganize the manuscript text** so that it is scientifically honest,
   clearly positioned, and realistically publishable.
3. Help the user build or refactor **analysis scripts** that correspond to what the
   manuscript actually claims (e.g., real TCGA survival, LLPS-related scores).

Always prefer:
- High scientific rigor and honesty over “selling” the story.
- Incremental, reviewable edits with diffs over large, destructive rewrites.
- Clear TODO markers instead of fabricating results or references.

---

## Repository assumptions

Assume (and adapt if filenames differ):

- `manuscript/main.tex` (or `main.md`): main manuscript text.
- `manuscript/figures/`: figures.
- `analysis/`:
  - `data_prep.py` or similar: TCGA expression processing.
  - `correlation_analysis.py`: PD-L1 vs regulators correlations.
  - `survival_simulation.py`: current simulated survival analysis (to be replaced or clearly downgraded).
- `data/`:
  - `tcga_expression/`: processed expression.
  - `tcga_clinical/`: real TCGA clinical data (to be wired into new survival scripts).
  - `llps_gene_sets/`: LLPS-related gene sets (may need to be added).

If actual filenames differ, FIRST infer the right files and update this mental map.

---

## Known scientific issues to fix

When asked to “audit” or “revise” the paper, you MUST explicitly reason about
at least the following categories and create issue IDs:

- **SURV-\***: Survival analysis and clinical interpretation.
- **LLPS-\***: LLPS framing vs what is actually quantified.
- **NOVEL-\***: Novelty claims and positioning vs existing literature.
- **METH-\***: Data processing choices and statistical methodology.
- **WRITE-\***: Writing, structure, clarity, and transparency.

### 1. SURV – Survival analysis

Current state (as of v1 of the manuscript):
- Survival analysis is based on **simulated clinical data**, not real TCGA OS/PFS.
- Abstract and Results text can be misread as if results came from real patients.
- Reported HRs, p-values, and C-index therefore **cannot be used for real clinical claims**.

Your goals:

- **Preferred fix**: Help the user create a new pipeline using **real TCGA clinical data**.
  - Create or extend scripts (e.g. `analysis/survival_tcga_real.py`):
    - Load real TCGA OS / PFS and covariates.
    - Fit Cox models / KM curves for PD-L1 and the four regulators.
    - Separate univariate and multivariate models.
    - Save reproducible outputs (tables/CSVs + plots).
  - Then adjust manuscript wording so that:
    - All survival results that come from real data are clearly labeled as such.
    - Any residual simulated analysis is clearly labeled as “proof-of-concept simulation” and
      **never used for clinical interpretation**.

- **Temporary / fallback fix** (if the user chooses to keep simulation only):
  - In Abstract, Methods, Results, and Discussion:
    - Explicitly state that survival results are from **simulated data only**.
    - Add a clear limitations paragraph that says these cannot support clinical conclusions.
  - Tone down any language suggesting real prognostic or predictive value.

You MUST NOT:
- Invent HRs, p-values, or C-index numbers if the scripts have not been run.
- Quietly treat simulated results as if they were real.

Instead, use clear placeholders such as `HR = XX (95% CI: XX–XX) [real TCGA analysis pending]`
or `TODO-SURV-REAL-DATA`.

---

### 2. LLPS – Framing vs actual analysis

Current mismatch:
- Title and framing emphasize “LLPS-associated” regulators.
- The actual computations are standard bulk expression correlations and survival,
  without any explicit LLPS-specific score or model.

Your goals:

1. **Align the framing with what is actually done**, OR
2. Extend the analysis so that there is at least **one LLPS-specific quantitative component**.

Possible LLPS-specific additions (do NOT fabricate data; create scripts, not fake results):

- Use LLPS gene sets (e.g., genes annotated in LLPS databases) to compute sample-level
  LLPS scores (e.g., ssGSEA / mean expression).
- Analyze:
  - LLPS score vs PD-L1 expression.
  - LLPS score vs the four regulators.
  - LLPS score vs immune infiltration.
- Add a short Results subsection like “LLPS-related transcriptomic patterns” **only after**
  there is a real script and real outputs.

If LLPS-specific analyses are not added:

- You MUST soften the title and claims:
  - Frame the work as “integrating known LLPS-related regulators of PD-L1”
    rather than establishing new LLPS mechanisms.
- Add explicit statements in the Discussion that:
  - The LLPS aspect is based on prior mechanistic literature, not on new direct measurements.
  - The current analysis focuses on transcriptomic correlates only.

---

### 3. NOVEL – Novelty and literature positioning

Facts to keep in mind:

- The mechanistic relationships CMTM6–PD-L1 and STUB1–PD-L1 are already well described
  experimentally in prior work.
- Many TCGA / pan-cancer papers already link PD-L1 expression, immune infiltration,
  and survival in various tumors.
- Some recent work has explored LLPS-related signatures in relation to immune checkpoints.

Your job is to:
- Position this paper as an **integrative, contextual, and robustness-focused** analysis,
  NOT as the first discovery of these regulators.
- Replace or edit over-strong claims like “no previous work has…” with accurate statements such as:
  - “Previous work has established X. Here we systematically contextualize X in
     a multi-cancer, confounder-adjusted TCGA framework.”

When suggesting references:
- Provide **paper titles + year + journal** as candidates.
- Use clear placeholders like `[REF-PLACEHOLDER: CMTM6 pan-cancer, 2020, journal name]`.
- Do NOT invent DOIs, PMIDs, or overly precise bibliographic details.

---

### 4. METH – Data and methods details

Key methodological considerations:

- Expression is currently processed as FPKM with ComBat batch correction.
- Batch sources must be described explicitly (centers/platforms/etc.).
- Immune deconvolution uses one method (e.g., TIMER2.0) only.
- Tumor purity is not explicitly modeled as a covariate.
- External validation (e.g., ICI cohorts) is missing but would be a strong plus.

Your goals:

- Ensure the Methods section:
  - Clearly explains the expression pipeline and justifies the choices.
  - Explicitly describes batch variables and ComBat usage.
  - Explicitly describes immune deconvolution method(s) and why they were chosen.
- Suggest (but do not assume) extensions such as:
  - Additional deconvolution methods.
  - Including tumor purity as a covariate.
  - External validation datasets.

When editing scripts:
- Prefer to add new analysis files (e.g., `*_alt.py`) rather than overwriting existing ones,
  unless the user asks you to refactor.
- Add docstrings and comments that explain:
  - Input expectations.
  - Outputs that the manuscript will rely on.

---

### 5. WRITE – Writing and structure

General writing rules:

- Scientific tone: precise, honest, and modest about claims.
- Make all limitations and caveats visible **early** (especially simulated survival).
- Avoid unnecessary “marketing” lines (e.g., bragging about CPU-hours)
  in the main text; move them to Supplementary or repository docs if needed.

When asked to revise text:

1. Work section-by-section (e.g., Abstract, Introduction, Methods, Results, Discussion).
2. For each section:
   - Summarize the current intent.
   - List the issues (SURV-*, LLPS-*, NOVEL-*, METH-*, WRITE-*).
   - Propose a numbered plan of edits.
   - THEN apply the edits, showing unified diffs where possible.

You should:
- Preserve correct technical content even while rephrasing.
- Add explicit “Limitations” and “Future work” subsections where appropriate.
- Insert `TODO-` comments rather than guessing numbers or results that the user hasn’t computed yet.

---

## Workflow rules for this project

When the user starts an interactive session and asks for help on this paper:

1. **Always start with an audit plan**
   - Read `manuscript/main.tex` (or `main.md`) and relevant analysis scripts.
   - Generate an issue list with IDs:
     - SURV-*, LLPS-*, NOVEL-*, METH-*, WRITE-*.
   - Sort them roughly by scientific severity (SURV and LLPS issues first).

2. **Confirm the plan with the user before large edits**
   - Present a concise summary:
     - What you will change.
     - Which files will be edited.
     - What new scripts or figures will be introduced.

3. **Edit in small, reviewable steps**
   - For manuscripts: show diffs for a subsection at a time.
   - For code: create or update files with clear comments and avoid breaking existing workflows.
   - Keep changes logically grouped (e.g., “SURV fixes”, “LLPS framing fixes”).

4. **Never fabricate scientific results**
   - If required numbers or analyses do not exist yet, create:
     - Clean, well-documented analysis scripts.
     - Skeleton text using neutral placeholders.
   - Mark them with `TODO-` comments so the user knows where to fill in real results.

5. **Document what you changed**
   - Keep a running “Changelog for this revision” section in a new file,
     e.g. `manuscript/REVISION_NOTES.md`, listing:
     - Date.
     - Issue IDs addressed.
     - Files touched.

---

## Style and language

- The user primarily interacts in **Traditional Chinese**, but the manuscript itself
  is in **English**. When editing manuscript files, always write in idiomatic scientific English.
- When explaining plans or summarizing changes in the chat, you may use Chinese if the
  user is speaking Chinese.
- Use standard immuno-oncology terminology and avoid colloquial expressions in the paper text.

---

## What to do when the user says “run a full revision”

Interpret it as:

1. Re-run the **audit** and update the issue list.
2. Propose an updated revision plan, in this order:
   - SURV (survival: real vs simulated).
   - LLPS (framing and possible new analyses).
   - NOVEL (positioning and references).
   - METH (methods clarification).
   - WRITE (clarity, structure, limitations).
3. Execute the plan in phases, checking in with the user between phases.
4. At the end, produce:
   - Updated manuscript file(s).
   - New or updated analysis scripts.
   - A brief summary of what changed and what is still TODO.

Always respect this CLAUDE.md as the authoritative instructions for this project.
