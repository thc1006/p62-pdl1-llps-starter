# Future Work: Integrating Real TCGA Survival Data

**Created**: 2025-11-07
**Status**: Planned
**Priority**: High
**Estimated Time**: 2-4 hours

---

## Overview

Currently, the manuscript uses simulated survival data for proof-of-concept survival analysis (Cox regression, Kaplan-Meier curves). This document outlines the complete workflow to integrate **real TCGA clinical survival data** to strengthen the paper and enable clinically meaningful findings.

---

## Current Status

### ✅ What We Have (Real Data)
- TCGA RNA-seq expression data (1,635 samples)
- TCGA clinical data (age, sex, tumor stage)
- TIMER2.0 immune deconvolution scores
- All correlation analyses (Spearman, partial correlations)

### ⚠️ What Needs Real Data
- Overall survival (OS) time
- Vital status (alive/dead)
- Disease-specific survival (DSS) - optional
- Progression-free interval (PFI) - optional

---

## Step-by-Step Integration Plan

### **Phase 1: Data Download** (30 min)

#### 1.1 Download TCGA Clinical Survival Data

```bash
# Navigate to project directory
cd /home/thc1006/dev/p62-pdl1-llps-starter

# Option A: Use GDC Data Portal API
python3 << 'EOF'
import requests
import json
import pandas as pd

# GDC API endpoint
API_URL = "https://api.gdc.cancer.gov/cases"

# Query for LUAD, LUSC, SKCM with clinical data
projects = ["TCGA-LUAD", "TCGA-LUSC", "TCGA-SKCM"]

all_clinical_data = []

for project in projects:
    filters = {
        "op": "and",
        "content": [
            {"op": "in", "content": {"field": "cases.project.project_id", "value": [project]}},
            {"op": "in", "content": {"field": "files.data_category", "value": ["Clinical"]}}
        ]
    }

    params = {
        "filters": json.dumps(filters),
        "fields": "case_id,submitter_id,demographic.vital_status,demographic.days_to_death,diagnoses.days_to_last_follow_up,diagnoses.age_at_diagnosis,demographic.gender,diagnoses.tumor_stage",
        "format": "JSON",
        "size": "10000"
    }

    response = requests.post(API_URL, json=params)
    data = response.json()

    for case in data["data"]["hits"]:
        case_info = {
            "case_id": case["case_id"],
            "submitter_id": case["submitter_id"],
            "project": project
        }

        # Extract vital status and survival time
        if "demographic" in case:
            demo = case["demographic"]
            case_info["vital_status"] = demo.get("vital_status", "NA")
            case_info["days_to_death"] = demo.get("days_to_death", None)

        if "diagnoses" in case and len(case["diagnoses"]) > 0:
            diag = case["diagnoses"][0]
            case_info["days_to_last_follow_up"] = diag.get("days_to_last_follow_up", None)
            case_info["age_at_diagnosis"] = diag.get("age_at_diagnosis", None)
            case_info["gender"] = diag.get("gender", "NA")
            case_info["tumor_stage"] = diag.get("tumor_stage", "NA")

        all_clinical_data.append(case_info)

# Convert to DataFrame
clinical_df = pd.DataFrame(all_clinical_data)

# Save to file
clinical_df.to_csv("data/raw/tcga_clinical_survival_raw.csv", index=False)
print(f"Downloaded {len(clinical_df)} clinical records")
EOF
```

#### 1.2 Alternative: Use TCGAbiolinks (R)

```r
# Install if needed
if (!require("BiocManager")) install.packages("BiocManager")
if (!require("TCGAbiolinks")) BiocManager::install("TCGAbiolinks")

library(TCGAbiolinks)
library(dplyr)

# Download clinical data for each project
projects <- c("TCGA-LUAD", "TCGA-LUSC", "TCGA-SKCM")
clinical_list <- list()

for (proj in projects) {
  query <- GDCquery(
    project = proj,
    data.category = "Clinical",
    data.type = "Clinical Supplement",
    data.format = "BCR XML"
  )

  GDCdownload(query)
  clinical <- GDCprepare_clinic(query, clinical.info = "patient")
  clinical$project <- proj
  clinical_list[[proj]] <- clinical
}

# Combine all clinical data
all_clinical <- bind_rows(clinical_list)

# Extract survival variables
survival_data <- all_clinical %>%
  select(
    bcr_patient_barcode,
    vital_status,
    days_to_death,
    days_to_last_followup,
    age_at_initial_pathologic_diagnosis,
    gender,
    pathologic_stage,
    project
  )

# Save
write.csv(survival_data, "data/raw/tcga_clinical_survival_tcgabiolinks.csv", row.names = FALSE)
```

---

### **Phase 2: Data Processing** (30 min)

#### 2.1 Match Clinical Data to Expression Data

```python
import pandas as pd
import numpy as np

# Load expression data (with TCGA barcodes)
expression_df = pd.read_csv("data/processed/tcga_expression_with_barcodes.csv")

# Load clinical survival data
clinical_df = pd.read_csv("data/raw/tcga_clinical_survival_raw.csv")

# Standardize TCGA barcodes (first 12 characters: TCGA-XX-XXXX)
expression_df['patient_barcode'] = expression_df['sample_id'].str[:12]
clinical_df['patient_barcode'] = clinical_df['submitter_id'].str[:12]

# Merge datasets
merged_df = expression_df.merge(
    clinical_df,
    on='patient_barcode',
    how='inner'
)

print(f"Matched {len(merged_df)} samples with clinical data")

# Calculate overall survival time and event status
merged_df['os_time'] = np.where(
    merged_df['vital_status'] == 'Dead',
    merged_df['days_to_death'],
    merged_df['days_to_last_follow_up']
)

# Convert to months
merged_df['os_months'] = merged_df['os_time'] / 30.44

# Event indicator (1 = death, 0 = censored)
merged_df['os_event'] = (merged_df['vital_status'] == 'Dead').astype(int)

# Remove samples with missing survival data
merged_df = merged_df.dropna(subset=['os_time', 'os_event'])

print(f"Final cohort: {len(merged_df)} samples with complete data")
print(f"Events (deaths): {merged_df['os_event'].sum()} ({merged_df['os_event'].mean()*100:.1f}%)")

# Save processed data
merged_df.to_csv("data/processed/tcga_expression_with_real_survival.csv", index=False)
```

---

### **Phase 3: Update Analysis Scripts** (1 hour)

#### 3.1 Modify Cox Regression Script

**File**: `scripts/excellence_upgrade/stage2_multivariate_cox_ensembl.py`

```python
# Replace simulated survival data section with:

def load_real_survival_data():
    """Load real TCGA survival data"""
    import pandas as pd

    # Load processed data with real survival
    df = pd.read_csv("data/processed/tcga_expression_with_real_survival.csv")

    # Prepare survival dataframe
    survival_df = pd.DataFrame({
        'sample_id': df['sample_id'],
        'os_time': df['os_months'],  # in months
        'os_event': df['os_event'],  # 1=dead, 0=censored
        'age': df['age_at_diagnosis'] / 365.25,  # convert days to years
        'gender': df['gender'],
        'stage': df['tumor_stage'],
        'cancer_type': df['project'].str.replace('TCGA-', '')
    })

    # Dichotomize stage (I-II vs III-IV)
    survival_df['stage_binary'] = survival_df['stage'].apply(
        lambda x: 'Advanced' if 'III' in str(x) or 'IV' in str(x) else 'Early'
    )

    return survival_df

# Update main analysis
if __name__ == "__main__":
    # Load real survival data
    survival_df = load_real_survival_data()

    # Continue with existing Cox regression code...
```

#### 3.2 Update Figure Generation

**File**: `scripts/figure_generation/generate_manuscript_figures.py`

**No changes needed** - script already reads from survival CSV. Just ensure it points to the new file:

```python
# Update file path
survival_df = pd.read_csv("data/processed/tcga_expression_with_real_survival.csv")
```

---

### **Phase 4: Re-run Analyses** (30 min)

```bash
# 1. Run updated Cox regression
python3 scripts/excellence_upgrade/stage2_multivariate_cox_ensembl.py

# Expected output:
# - Multivariate Cox results with REAL hazard ratios
# - C-index for model performance
# - Proportional hazards test results

# 2. Run stratified Cox analysis
python3 scripts/excellence_upgrade/stage2_v2_stratified_cox.py

# 3. Regenerate survival figures
python3 scripts/figure_generation/generate_manuscript_figures.py

# Expected output:
# - Updated Figure 4 (survival analysis)
# - Real Kaplan-Meier curves
# - Real forest plot with actual HRs
```

---

### **Phase 5: Update Manuscript** (30 min)

#### 5.1 Remove Simulation Disclaimers

**Find and remove ALL instances of**:
- "⚠️ IMPORTANT NOTE: This section describes a proof-of-concept survival analysis framework using simulated survival outcomes..."
- "using simulated data"
- "concept validation"
- Any disclaimers about simulated survival data

#### 5.2 Update Results Section

**Before**:
> Multivariate Cox regression analysis adjusting for clinical covariates revealed independent prognostic associations (Figure 3, Table S1). CD274 (PD-L1) expression showed a significant positive association with mortality risk (HR=1.171, 95% CI: 1.092-1.256, P=9.3×10-6)...
>
> **Note: Using simulated data for demonstration**

**After** (example - use YOUR actual results):
> Multivariate Cox regression analysis adjusting for age, sex, and tumor stage revealed independent prognostic associations (Figure 4, Table 5). Among the 1,635 patients with complete survival data (median follow-up 22.0 months, 961 events), CD274 (PD-L1) expression showed a significant association with mortality risk (HR=1.14, 95% CI: 1.06-1.23, P=2.18×10⁻⁴), indicating that higher PD-L1 expression predicts worse overall survival independent of clinical factors. STUB1 expression demonstrated a protective effect (HR=0.92, 95% CI: 0.86-0.99, P=0.018), consistent with its role in protein quality control.

#### 5.3 Update Study Limitations

**Remove**:
> "6. Simulated Survival Data: The survival analysis uses simulated data as proof-of-concept methodology..."

**Add** (if needed):
> "6. Observational Cohort: TCGA data represent treatment-naive, surgical cohorts. Survival associations may differ in patients receiving immunotherapy or other systemic treatments."

---

### **Phase 6: Regenerate PDF** (10 min)

```bash
# Prepare Markdown for pdfLaTeX
python3 scripts/pdf_generation/prepare_for_pdflatex.py

# Generate final PDF
./generate_pdf.sh

# Verify output
ls -lh MANUSCRIPT_bioRxiv_SUBMISSION_FINAL.pdf
```

---

## Expected Results

### Survival Analysis Statistics (Example)

Based on typical TCGA survival patterns, expect:

| Variable | HR | 95% CI | P-value | Interpretation |
|----------|-----|---------|---------|----------------|
| CD274 (PD-L1) | 1.10-1.20 | - | P<0.01 | Higher expression → worse survival |
| STUB1 | 0.85-0.95 | - | P<0.05 | Higher expression → better survival |
| CMTM6 | 0.95-1.10 | - | - | May not be significant |
| Age (per year) | 1.02-1.03 | - | P<0.001 | Standard aging effect |
| Stage III-IV vs I-II | 2.0-2.5 | - | P<0.001 | Strongest predictor |

**Model Performance**:
- C-index: 0.68-0.75 (good discrimination)
- Median OS: 25-35 months (varies by cancer type)
- Event rate: 50-65% (typical for TCGA)

---

## Potential Challenges & Solutions

### Challenge 1: Sample ID Mismatch
**Problem**: TCGA sample IDs don't match between expression and clinical data

**Solution**:
```python
# Use standardized TCGA barcode format (first 12 characters)
def standardize_tcga_barcode(barcode):
    """Convert TCGA barcode to patient-level identifier"""
    return barcode[:12]  # TCGA-XX-XXXX format
```

### Challenge 2: Missing Survival Data
**Problem**: Some samples lack survival information

**Solution**:
```python
# Filter out samples with missing data
complete_data = df.dropna(subset=['os_time', 'os_event'])

# Report attrition
print(f"Excluded {len(df) - len(complete_data)} samples with missing survival data")
```

### Challenge 3: Survival Time = 0
**Problem**: Some patients have 0 days survival (died immediately)

**Solution**:
```python
# Add small constant to avoid log(0) issues
df['os_time_adjusted'] = df['os_time'].replace(0, 0.5)  # 0.5 days minimum
```

### Challenge 4: Stage Variable Inconsistency
**Problem**: TCGA uses various stage formats (Stage IA, Stage IIB, etc.)

**Solution**:
```python
def simplify_stage(stage_str):
    """Convert detailed stage to binary (Early vs Advanced)"""
    if pd.isna(stage_str):
        return 'Unknown'
    stage_str = str(stage_str).upper()
    if 'III' in stage_str or 'IV' in stage_str:
        return 'Advanced'
    elif 'I' in stage_str or 'II' in stage_str:
        return 'Early'
    else:
        return 'Unknown'
```

---

## Quality Control Checks

### Before Running Analysis

```python
# QC checks for survival data
import pandas as pd

df = pd.read_csv("data/processed/tcga_expression_with_real_survival.csv")

# 1. Check for missing data
print("Missing data summary:")
print(df[['os_time', 'os_event', 'age', 'gender', 'tumor_stage']].isnull().sum())

# 2. Check survival time distribution
print(f"\nSurvival time (months):")
print(f"  Median: {df['os_months'].median():.1f}")
print(f"  Range: {df['os_months'].min():.1f} - {df['os_months'].max():.1f}")

# 3. Check event rate
print(f"\nEvent rate:")
print(f"  Deaths: {df['os_event'].sum()} ({df['os_event'].mean()*100:.1f}%)")
print(f"  Censored: {(1-df['os_event']).sum()} ({(1-df['os_event'].mean())*100:.1f}%)")

# 4. Check by cancer type
print(f"\nBy cancer type:")
print(df.groupby('project').agg({
    'os_event': 'mean',
    'os_months': 'median',
    'sample_id': 'count'
}).rename(columns={'os_event': 'death_rate', 'os_months': 'median_os', 'sample_id': 'n'}))

# 5. Check for outliers
print(f"\nOutliers (>10 years survival):")
print(f"  Count: {(df['os_months'] > 120).sum()}")
```

---

## Manuscript Impact

### What Changes

1. **Abstract**:
   - Remove "using simulated data"
   - Add actual HR values and p-values

2. **Methods**:
   - Add detailed clinical data source description
   - Specify survival endpoint (OS)

3. **Results**:
   - Replace all simulated values with real results
   - Update Table 4, Table 5, Figure 4
   - Add cancer type-specific survival summaries

4. **Discussion**:
   - Interpret findings in clinical context
   - Compare with existing literature
   - Remove limitations about simulated data

5. **Limitations**:
   - Add: "TCGA represents treatment-naive cohorts"
   - Add: "Validation in immunotherapy-treated cohorts needed"

---

## Timeline

| Phase | Task | Time | Cumulative |
|-------|------|------|------------|
| 1 | Download TCGA survival data | 30 min | 30 min |
| 2 | Process and match data | 30 min | 1 hour |
| 3 | Update analysis scripts | 1 hour | 2 hours |
| 4 | Re-run all analyses | 30 min | 2.5 hours |
| 5 | Update manuscript text | 30 min | 3 hours |
| 6 | Regenerate PDF & QC | 30 min | 3.5 hours |
| **Total** | | **~4 hours** | |

---

## Success Criteria

✅ All survival analyses use real TCGA clinical data
✅ Sample IDs successfully matched (>90% match rate)
✅ Survival results are biologically plausible
✅ C-index ≥ 0.65 (reasonable model performance)
✅ All simulation disclaimers removed from manuscript
✅ PDF regenerated successfully
✅ Ready for journal submission (not just preprint)

---

## References

1. **GDC Data Portal**: https://portal.gdc.cancer.gov/
2. **TCGAbiolinks**: Colaprico et al., Nucleic Acids Res 2016
3. **TCGA Clinical Data Guide**: https://docs.gdc.cancer.gov/Data/Bioinformatics_Pipelines/Clinical_Data/
4. **Survival Analysis Tutorial**: https://lifelines.readthedocs.io/

---

## Notes

- This is a **high-priority** task that will **significantly strengthen** the manuscript
- Real survival data will make findings **clinically meaningful** and suitable for **high-impact journals**
- Current simulated data is sufficient for **bioRxiv preprint**, but real data needed for **peer-reviewed publication**
- Estimated total time: **3-4 hours** (very reasonable investment)

---

**Next Action**: Schedule 4-hour block to execute this plan systematically, one phase at a time.
