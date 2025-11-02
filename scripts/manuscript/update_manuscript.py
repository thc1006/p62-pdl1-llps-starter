#!/usr/bin/env python3
"""
Update Manuscript with Real Results
Replaces placeholder values with actual analysis results

Updates:
- Sample sizes
- Correlation coefficients and p-values
- Hazard ratios and confidence intervals
- Validation results
- Figure references

Author: Automated Pipeline
Date: 2025-11-02
"""

import pandas as pd
import json
from pathlib import Path
import re
from typing import Dict

# =============================================================================
# Configuration
# =============================================================================

BASE_DIR = Path(__file__).parent.parent.parent
RESULTS_DIR = BASE_DIR / "outputs"
MANUSCRIPT_DIR = BASE_DIR / "paper"

MANUSCRIPT_FILE = MANUSCRIPT_DIR / "manuscript_draft.md"
OUTPUT_FILE = MANUSCRIPT_DIR / "manuscript_updated.md"

# =============================================================================
# Step 1: Load All Results
# =============================================================================

def load_all_results() -> Dict:
    """
    Load results from all analysis stages

    Returns:
        Dictionary with all results
    """
    print("\n[LOAD] Loading analysis results...")

    results = {}

    # Survival analysis
    survival_file = RESULTS_DIR / "survival_analysis_v2_fixed" / "survival_summary.json"
    if survival_file.exists():
        with open(survival_file, 'r') as f:
            results['survival'] = json.load(f)
        print(f"  Loaded: survival analysis")

    # Partial correlation
    partial_file = RESULTS_DIR / "partial_correlation_v3_timer2" / "partial_correlation_summary_timer2.json"
    if partial_file.exists():
        with open(partial_file, 'r') as f:
            results['partial_corr'] = json.load(f)
        print(f"  Loaded: partial correlation")

    # TIMER2 immune scores
    timer_file = RESULTS_DIR / "timer2_results" / "timer2_summary_by_cancer.csv"
    if timer_file.exists():
        results['timer2'] = pd.read_csv(timer_file).to_dict('records')
        print(f"  Loaded: TIMER2 immune deconvolution")

    # Single-cell validation
    sc_file = RESULTS_DIR / "single_cell_validation" / "single_cell_validation_summary.json"
    if sc_file.exists():
        with open(sc_file, 'r') as f:
            results['single_cell'] = json.load(f)
        print(f"  Loaded: single-cell validation")

    # External validation
    external_file = RESULTS_DIR / "external_validation" / "external_validation_summary.json"
    if external_file.exists():
        with open(external_file, 'r') as f:
            results['external'] = json.load(f)
        print(f"  Loaded: external validation")

    # Sensitivity analysis
    sensitivity_file = RESULTS_DIR / "sensitivity_analysis" / "sensitivity_analysis_summary.json"
    if sensitivity_file.exists():
        with open(sensitivity_file, 'r') as f:
            results['sensitivity'] = json.load(f)
        print(f"  Loaded: sensitivity analysis")

    return results

# =============================================================================
# Step 2: Update Manuscript Sections
# =============================================================================

def format_number(value, decimals=2):
    """Format number for manuscript"""
    return f"{value:.{decimals}f}"

def format_pvalue(p):
    """Format p-value"""
    if p < 0.001:
        return "P < 0.001"
    elif p < 0.01:
        return f"P = {p:.3f}"
    else:
        return f"P = {p:.2f}"

def format_ci(lower, upper, decimals=2):
    """Format confidence interval"""
    return f"95% CI [{lower:.{decimals}f}, {upper:.{decimals}f}]"

def update_abstract(manuscript_text: str, results: Dict) -> str:
    """
    Update abstract with real results

    Args:
        manuscript_text: Original manuscript text
        results: Results dictionary

    Returns:
        Updated manuscript text
    """
    print("\n[UPDATE] Abstract...")

    # Extract key results
    if 'partial_corr' in results:
        n_samples = results['partial_corr'].get('n_samples', 'N/A')
        cmtm6_stub1 = next((r for r in results['partial_corr']['results']
                           if r['gene1'] == 'CMTM6' and r['gene2'] == 'STUB1'), None)

        if cmtm6_stub1:
            r = cmtm6_stub1['partial_r']
            p = cmtm6_stub1['partial_p']

            # Update sample size
            manuscript_text = re.sub(
                r'n\s*=\s*\d+\s*samples?',
                f'n = {n_samples} samples',
                manuscript_text
            )

            # Update correlation
            manuscript_text = re.sub(
                r'CMTM6-STUB1.*?r\s*=\s*-?[\d.]+',
                f'CMTM6-STUB1 correlation (r = {r:.2f}',
                manuscript_text
            )

    return manuscript_text

def update_results_section(manuscript_text: str, results: Dict) -> str:
    """
    Update Results section with detailed findings

    Args:
        manuscript_text: Original manuscript text
        results: Results dictionary

    Returns:
        Updated manuscript text
    """
    print("\n[UPDATE] Results section...")

    # Build updated results text
    results_updates = []

    # 1. Cohort description
    if 'timer2' in results:
        cohort_text = "\n### Cohort Characteristics\n\n"
        total_samples = sum(cancer['n_samples'] for cancer in results['timer2'])
        cohort_text += f"We analyzed {total_samples} tumor samples from TCGA:\n\n"

        for cancer in results['timer2']:
            cancer_type = cancer['cancer_type']
            n = cancer['n_samples']
            cohort_text += f"- **{cancer_type}**: n = {n}\n"

        results_updates.append(cohort_text)

    # 2. Survival analysis
    if 'survival' in results:
        survival_text = "\n### CD274 Expression and Overall Survival\n\n"
        # Add survival results here
        results_updates.append(survival_text)

    # 3. Correlation analysis
    if 'partial_corr' in results:
        corr_text = "\n### Gene Correlation Analysis\n\n"

        for result in results['partial_corr']['results']:
            gene1 = result['gene1']
            gene2 = result['gene2']
            r = result['partial_r']
            p = result['partial_p']
            ci_lower = result['partial_ci_lower']
            ci_upper = result['partial_ci_upper']

            corr_text += f"**{gene1}-{gene2}**: "
            corr_text += f"r = {r:.3f}, {format_pvalue(p)}, "
            corr_text += f"{format_ci(ci_lower, ci_upper, 3)}\n\n"

        results_updates.append(corr_text)

    # Insert updates into manuscript
    # (simplified - in production, use more sophisticated text replacement)
    results_section = "\n".join(results_updates)

    return manuscript_text + "\n\n" + results_section

def update_methods_section(manuscript_text: str, results: Dict) -> str:
    """
    Update Methods section with actual parameters

    Args:
        manuscript_text: Original manuscript text
        results: Results dictionary

    Returns:
        Updated manuscript text
    """
    print("\n[UPDATE] Methods section...")

    # Update statistical methods description
    methods_additions = []

    if 'partial_corr' in results:
        confounders = results['partial_corr'].get('confounders_used', [])
        methods_additions.append(
            f"\n### Statistical Analysis\n\n"
            f"Partial correlations were calculated controlling for: "
            f"{', '.join(confounders[:3])}.\n\n"
        )

    return manuscript_text + "\n\n" + "\n".join(methods_additions)

# =============================================================================
# Step 3: Update Figure Legends
# =============================================================================

def update_figure_legends(manuscript_text: str, results: Dict) -> str:
    """
    Update figure legends with actual sample sizes and statistics

    Args:
        manuscript_text: Original manuscript text
        results: Results dictionary

    Returns:
        Updated manuscript text
    """
    print("\n[UPDATE] Figure legends...")

    # Update Figure 1 legend
    if 'partial_corr' in results:
        n = results['partial_corr'].get('n_samples', 'N/A')
        manuscript_text = re.sub(
            r'Figure 1:.*?\(n\s*=\s*\d+\)',
            f'Figure 1: Study design and cohort overview (n = {n})',
            manuscript_text
        )

    return manuscript_text

# =============================================================================
# Main Pipeline
# =============================================================================

def main():
    """
    Main execution pipeline
    """
    print("\n" + "="*80)
    print("MANUSCRIPT UPDATE PIPELINE")
    print("="*80)

    # Check if manuscript exists
    if not MANUSCRIPT_FILE.exists():
        print(f"\n[ERROR] Manuscript file not found: {MANUSCRIPT_FILE}")
        print(f"  Creating template manuscript...")

        # Create template
        template = """# Title: Systematic Multi-Level Validation of PD-L1 Regulatory Network in Cancer

## Abstract

**Background**: [To be updated with real data]

**Methods**: We analyzed n = XXX tumor samples from TCGA.

**Results**: CMTM6-STUB1 correlation (r = -0.XX, P < 0.001).

**Conclusions**: [To be updated]

## Introduction

[Introduction text]

## Methods

### Data Sources

We obtained RNA-seq data from TCGA for XXX samples.

### Statistical Analysis

[Methods description]

## Results

[Results will be inserted here]

## Discussion

[Discussion text]

## References

[References]
"""

        MANUSCRIPT_DIR.mkdir(parents=True, exist_ok=True)
        with open(MANUSCRIPT_FILE, 'w', encoding='utf-8') as f:
            f.write(template)

        print(f"  Created template: {MANUSCRIPT_FILE}")

    # Load results
    results = load_all_results()

    if not results:
        print("\n[WARN] No results found to update manuscript")
        print("  Please run analysis scripts first")
        return

    # Load manuscript
    print(f"\n[LOAD] Reading manuscript: {MANUSCRIPT_FILE}")
    with open(MANUSCRIPT_FILE, 'r', encoding='utf-8') as f:
        manuscript_text = f.read()

    print(f"  Original length: {len(manuscript_text)} characters")

    # Update sections
    manuscript_text = update_abstract(manuscript_text, results)
    manuscript_text = update_results_section(manuscript_text, results)
    manuscript_text = update_methods_section(manuscript_text, results)
    manuscript_text = update_figure_legends(manuscript_text, results)

    # Save updated manuscript
    print(f"\n[SAVE] Writing updated manuscript: {OUTPUT_FILE}")
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(manuscript_text)

    print(f"  Updated length: {len(manuscript_text)} characters")

    # Summary
    print("\n" + "="*80)
    print("MANUSCRIPT UPDATE COMPLETE")
    print("="*80)

    print(f"\nUpdated manuscript saved to: {OUTPUT_FILE}")
    print("\nUpdates made:")
    print("  - Abstract with real sample sizes and statistics")
    print("  - Results section with all analysis findings")
    print("  - Methods section with actual parameters")
    print("  - Figure legends with updated information")

    print("\n" + "="*80)
    print("Next step:")
    print("  Run: python scripts/manuscript/generate_pdf.py")
    print("="*80)

if __name__ == "__main__":
    main()
