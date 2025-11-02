#!/usr/bin/env python3
"""
Prepare Supplementary Materials for Submission
Organizes all supplementary tables, figures, and data files

Includes:
- Supplementary Tables (all correlation results, validation data)
- Supplementary Figures (per-cancer analyses, sensitivity)
- Supplementary Data Files (expression matrices, clinical data)

Author: Automated Pipeline
Date: 2025-11-02
"""

import pandas as pd
import shutil
from pathlib import Path
import json

# =============================================================================
# Configuration
# =============================================================================

BASE_DIR = Path(__file__).parent.parent.parent
RESULTS_DIR = BASE_DIR / "outputs"
OUTPUT_DIR = BASE_DIR / "outputs" / "supplementary_materials"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Directories
TABLES_DIR = OUTPUT_DIR / "tables"
FIGURES_DIR = OUTPUT_DIR / "figures"
DATA_DIR = OUTPUT_DIR / "data_files"

for dir in [TABLES_DIR, FIGURES_DIR, DATA_DIR]:
    dir.mkdir(parents=True, exist_ok=True)

# =============================================================================
# Step 1: Prepare Supplementary Tables
# =============================================================================

def prepare_supplementary_tables():
    """
    Compile all supplementary tables

    Tables:
    - S1: Complete correlation results
    - S2: Survival analysis by cancer type
    - S3: External validation results
    - S4: Single-cell validation results
    - S5: Sensitivity analyses
    """
    print("\n[TABLES] Preparing supplementary tables...")

    # Table S1: Correlation results
    partial_file = RESULTS_DIR / "partial_correlation_v3_timer2" / "partial_correlation_results_timer2.csv"
    if partial_file.exists():
        df = pd.read_csv(partial_file)

        # Format for publication
        df_pub = df[['gene1', 'gene2', 'n_samples', 'simple_r', 'simple_p',
                    'partial_r', 'partial_p', 'partial_ci_lower', 'partial_ci_upper']].copy()

        df_pub.columns = [
            'Gene 1', 'Gene 2', 'N', 'Simple r', 'Simple P',
            'Partial r', 'Partial P', '95% CI Lower', '95% CI Upper'
        ]

        # Format p-values
        df_pub['Simple P'] = df_pub['Simple P'].apply(lambda x: f"{x:.2e}")
        df_pub['Partial P'] = df_pub['Partial P'].apply(lambda x: f"{x:.2e}")

        # Save
        output_file = TABLES_DIR / "Table_S1_correlation_results.csv"
        df_pub.to_csv(output_file, index=False)
        print(f"  Saved: {output_file.name}")

        # Also save as Excel
        excel_file = TABLES_DIR / "Table_S1_correlation_results.xlsx"
        df_pub.to_excel(excel_file, index=False, sheet_name='Correlation Results')
        print(f"  Saved: {excel_file.name}")

    # Table S2: Per-cancer survival
    survival_file = RESULTS_DIR / "survival_analysis_v2_fixed" / "cox_results_per_cancer.csv"
    if survival_file.exists():
        df = pd.read_csv(survival_file)

        output_file = TABLES_DIR / "Table_S2_survival_per_cancer.csv"
        df.to_csv(output_file, index=False)
        print(f"  Saved: {output_file.name}")

    # Table S3: External validation
    external_file = RESULTS_DIR / "external_validation" / "meta_analysis_results.csv"
    if external_file.exists():
        df = pd.read_csv(external_file)

        output_file = TABLES_DIR / "Table_S3_external_validation.csv"
        df.to_csv(output_file, index=False)
        print(f"  Saved: {output_file.name}")

    # Table S4: Single-cell validation
    sc_file = RESULTS_DIR / "single_cell_validation" / "single_cell_correlations.csv"
    if sc_file.exists():
        df = pd.read_csv(sc_file)

        output_file = TABLES_DIR / "Table_S4_single_cell_validation.csv"
        df.to_csv(output_file, index=False)
        print(f"  Saved: {output_file.name}")

    # Table S5: Sensitivity analyses
    sensitivity_file = RESULTS_DIR / "sensitivity_analysis" / "bootstrap_stability_results.csv"
    if sensitivity_file.exists():
        df = pd.read_csv(sensitivity_file)

        output_file = TABLES_DIR / "Table_S5_sensitivity_analysis.csv"
        df.to_csv(output_file, index=False)
        print(f"  Saved: {output_file.name}")

# =============================================================================
# Step 2: Prepare Supplementary Figures
# =============================================================================

def prepare_supplementary_figures():
    """
    Copy and organize supplementary figures

    Figures:
    - S1: Per-cancer correlation plots
    - S2: Immune infiltration by cancer type
    - S3: Bootstrap stability distributions
    - S4: Alternative correlation methods
    """
    print("\n[FIGURES] Organizing supplementary figures...")

    # Copy all figures from outputs
    figure_sources = [
        (RESULTS_DIR / "figures_publication", "main_figures"),
        (RESULTS_DIR / "single_cell_validation", "single_cell"),
        (RESULTS_DIR / "external_validation", "external"),
        (RESULTS_DIR / "sensitivity_analysis", "sensitivity")
    ]

    copied_count = 0

    for source_dir, category in figure_sources:
        if not source_dir.exists():
            continue

        for fig_file in source_dir.glob("*.png"):
            dest_file = FIGURES_DIR / f"{category}_{fig_file.name}"
            shutil.copy2(fig_file, dest_file)
            copied_count += 1

    print(f"  Copied {copied_count} figures")

# =============================================================================
# Step 3: Prepare Data Files
# =============================================================================

def prepare_data_files():
    """
    Organize data files for supplementary materials

    Includes:
    - Expression matrices (subset for key genes)
    - Clinical data summary
    - Immune deconvolution results
    """
    print("\n[DATA] Preparing data files...")

    # Expression data (key genes only)
    expr_file = RESULTS_DIR / "tcga_full_cohort_real" / "expression_matrix_full_real.csv"
    if expr_file.exists():
        df = pd.read_csv(expr_file)

        # Keep only key genes + metadata
        key_genes = ['CD274', 'CMTM6', 'HIP1R', 'SQSTM1', 'STUB1', 'CMTM4']
        metadata_cols = ['sample_id', 'cancer_type']

        cols_to_keep = metadata_cols + [g for g in key_genes if g in df.columns]
        df_subset = df[cols_to_keep]

        output_file = DATA_DIR / "Data_S1_expression_key_genes.csv"
        df_subset.to_csv(output_file, index=False)
        print(f"  Saved: {output_file.name}")

    # Clinical data
    clinical_file = RESULTS_DIR / "tcga_full_cohort_real" / "clinical_data_full_real.csv"
    if clinical_file.exists():
        df = pd.read_csv(clinical_file)

        # Remove identifiable information
        cols_to_keep = ['sample_id', 'cancer_type', 'OS_status', 'OS_days',
                       'age_at_diagnosis', 'gender', 'tumor_stage_clean']

        df_subset = df[[c for c in cols_to_keep if c in df.columns]]

        output_file = DATA_DIR / "Data_S2_clinical_summary.csv"
        df_subset.to_csv(output_file, index=False)
        print(f"  Saved: {output_file.name}")

    # TIMER2 immune scores
    timer_file = RESULTS_DIR / "timer2_results" / "timer2_immune_scores.csv"
    if timer_file.exists():
        df = pd.read_csv(timer_file)

        output_file = DATA_DIR / "Data_S3_immune_deconvolution.csv"
        df.to_csv(output_file, index=False)
        print(f"  Saved: {output_file.name}")

# =============================================================================
# Step 4: Create README
# =============================================================================

def create_readme():
    """
    Create README for supplementary materials
    """
    print("\n[README] Creating supplementary materials guide...")

    readme_content = """# Supplementary Materials

## Contents

### Supplementary Tables
- **Table S1**: Complete correlation analysis results
- **Table S2**: Survival analysis by cancer type
- **Table S3**: External cohort validation (meta-analysis)
- **Table S4**: Single-cell validation results
- **Table S5**: Sensitivity and stability analyses

### Supplementary Figures
- **Figure S1-SX**: Additional analyses and validations

### Supplementary Data Files
- **Data S1**: Expression data for key genes (CD274, CMTM6, HIP1R, SQSTM1, STUB1)
- **Data S2**: Clinical data summary
- **Data S3**: Immune deconvolution results (TIMER2.0)

## File Formats
- Tables: CSV and Excel formats
- Figures: PNG (300 DPI)
- Data: CSV format

## Usage
All data files can be opened with standard spreadsheet software (Excel, LibreOffice)
or loaded into R/Python for further analysis.

## Citation
Please cite the main manuscript when using these materials.

## Contact
For questions about the data, please contact the corresponding author.
"""

    readme_file = OUTPUT_DIR / "README.md"
    with open(readme_file, 'w', encoding='utf-8') as f:
        f.write(readme_content)

    print(f"  Saved: {readme_file.name}")

# =============================================================================
# Main Pipeline
# =============================================================================

def main():
    """
    Main execution pipeline
    """
    print("\n" + "="*80)
    print("SUPPLEMENTARY MATERIALS PREPARATION PIPELINE")
    print("="*80)

    # Prepare all components
    prepare_supplementary_tables()
    prepare_supplementary_figures()
    prepare_data_files()
    create_readme()

    # Summary
    print("\n" + "="*80)
    print("SUPPLEMENTARY MATERIALS COMPLETE")
    print("="*80)

    print(f"\nAll materials saved to: {OUTPUT_DIR}")

    # Count files
    n_tables = len(list(TABLES_DIR.glob("*")))
    n_figures = len(list(FIGURES_DIR.glob("*.png")))
    n_data = len(list(DATA_DIR.glob("*")))

    print(f"\nSummary:")
    print(f"  Tables: {n_tables}")
    print(f"  Figures: {n_figures}")
    print(f"  Data files: {n_data}")

    print("\n" + "="*80)
    print("Next step:")
    print("  Run: python scripts/submission/create_submission_package.py")
    print("="*80)

if __name__ == "__main__":
    main()
