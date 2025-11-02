#!/usr/bin/env python3
"""
Create Complete Submission Package
Bundles manuscript, figures, supplementary materials, and code for journal submission

Package Contents:
1. Main manuscript (PDF + source)
2. Main figures (all panels, high-res)
3. Supplementary materials (tables, figures, data)
4. Cover letter template
5. Code repository (optional)

Author: Automated Pipeline
Date: 2025-11-02
"""

import zipfile
import shutil
from pathlib import Path
from datetime import datetime
import json

# =============================================================================
# Configuration
# =============================================================================

BASE_DIR = Path(__file__).parent.parent.parent
MANUSCRIPT_DIR = BASE_DIR / "paper"
FIGURES_DIR = BASE_DIR / "outputs" / "figures_publication"
SUPPLEMENTARY_DIR = BASE_DIR / "outputs" / "supplementary_materials"
OUTPUT_DIR = BASE_DIR / "outputs" / "submission_package"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

TIMESTAMP = datetime.now().strftime("%Y%m%d")
PACKAGE_NAME = f"PD-L1_Regulatory_Network_Submission_{TIMESTAMP}"

# =============================================================================
# Step 1: Organize Package Structure
# =============================================================================

def create_package_structure():
    """
    Create organized directory structure for submission

    Structure:
    submission_package/
    ├── 1_manuscript/
    ├── 2_main_figures/
    ├── 3_supplementary_materials/
    ├── 4_cover_letter/
    └── 5_code/ (optional)
    """
    print("\n[STRUCTURE] Creating package directories...")

    package_dir = OUTPUT_DIR / PACKAGE_NAME

    dirs = {
        'manuscript': package_dir / "1_manuscript",
        'figures': package_dir / "2_main_figures",
        'supplementary': package_dir / "3_supplementary_materials",
        'cover': package_dir / "4_cover_letter",
        'code': package_dir / "5_code"
    }

    for dir_name, dir_path in dirs.items():
        dir_path.mkdir(parents=True, exist_ok=True)
        print(f"  Created: {dir_name}/")

    return package_dir, dirs

# =============================================================================
# Step 2: Copy Manuscript Files
# =============================================================================

def copy_manuscript_files(dest_dir: Path):
    """
    Copy manuscript files

    Args:
        dest_dir: Destination directory
    """
    print("\n[MANUSCRIPT] Copying manuscript files...")

    files_to_copy = [
        (MANUSCRIPT_DIR / "manuscript_final.pdf", "manuscript_final.pdf"),
        (MANUSCRIPT_DIR / "manuscript_updated.md", "manuscript_source.md"),
        (MANUSCRIPT_DIR / "manuscript_final.html", "manuscript_preview.html")
    ]

    copied = 0
    for src, dest_name in files_to_copy:
        if src.exists():
            dest = dest_dir / dest_name
            shutil.copy2(src, dest)
            print(f"  Copied: {dest_name}")
            copied += 1

    if copied == 0:
        print("  [WARN] No manuscript files found")
        print("  Please run: python scripts/manuscript/generate_pdf.py")

# =============================================================================
# Step 3: Copy Main Figures
# =============================================================================

def copy_main_figures(dest_dir: Path):
    """
    Copy main figures (Figure 1-4)

    Args:
        dest_dir: Destination directory
    """
    print("\n[FIGURES] Copying main figures...")

    if not FIGURES_DIR.exists():
        print("  [WARN] Figures directory not found")
        print("  Please run: python scripts/figures/generate_all_figures.py")
        return

    # Copy main figures
    copied = 0
    for fig_file in sorted(FIGURES_DIR.glob("Figure*.png")):
        dest = dest_dir / fig_file.name
        shutil.copy2(fig_file, dest)
        print(f"  Copied: {fig_file.name}")
        copied += 1

    print(f"  Total: {copied} figures")

# =============================================================================
# Step 4: Copy Supplementary Materials
# =============================================================================

def copy_supplementary_materials(dest_dir: Path):
    """
    Copy all supplementary materials

    Args:
        dest_dir: Destination directory
    """
    print("\n[SUPPLEMENTARY] Copying supplementary materials...")

    if not SUPPLEMENTARY_DIR.exists():
        print("  [WARN] Supplementary directory not found")
        print("  Please run: python scripts/submission/prepare_supplementary.py")
        return

    # Copy entire supplementary directory structure
    for item in SUPPLEMENTARY_DIR.iterdir():
        if item.is_dir():
            dest = dest_dir / item.name
            shutil.copytree(item, dest, dirs_exist_ok=True)
            n_files = len(list(dest.rglob("*")))
            print(f"  Copied: {item.name}/ ({n_files} files)")
        else:
            dest = dest_dir / item.name
            shutil.copy2(item, dest)
            print(f"  Copied: {item.name}")

# =============================================================================
# Step 5: Create Cover Letter
# =============================================================================

def create_cover_letter(dest_dir: Path):
    """
    Create cover letter template

    Args:
        dest_dir: Destination directory
    """
    print("\n[COVER] Creating cover letter template...")

    cover_letter = f"""
Date: {datetime.now().strftime("%B %d, %Y")}

To the Editor,

We are pleased to submit our manuscript entitled:
**"Systematic Multi-Level Validation of PD-L1 Regulatory Network in Cancer"**
for consideration for publication in [JOURNAL NAME].

## Study Overview

In this computational study, we performed systematic multi-level validation of
the PD-L1 regulatory network across multiple cancer types using:

- TCGA bulk RNA-seq data (n = XXX samples, 3 cancer types)
- CPTAC proteomics validation (n = 219)
- Single-cell RNA-seq validation (TISCH2)
- External cohort validation (GEO, n = 621)
- Comprehensive sensitivity analyses

## Key Findings

1. **CMTM6-STUB1 Negative Correlation**: We validated the negative correlation
   between CMTM6 and STUB1 (partial r = -0.XX, P < 0.001) after controlling
   for immune infiltration.

2. **Survival Association**: CD274 expression associated with overall survival
   (HR = 1.XX, 95% CI [X.XX, X.XX], P < 0.01).

3. **Multi-level Concordance**: Findings replicated across bulk RNA-seq,
   proteomics, single-cell, and external cohorts.

## Novelty and Significance

This work represents the first systematic multi-level validation of the
PD-L1 regulatory network integrating:
- Immune-adjusted correlation analysis
- Multi-omics validation
- Cross-cancer type replication

## Suggested Reviewers

[Add 3-5 suggested reviewers with expertise in:
- Cancer immunology
- Bioinformatics/computational biology
- PD-L1 biology]

## Conflicts of Interest

The authors declare no conflicts of interest.

## Authorship

All authors have read and approved the manuscript and meet ICMJE criteria
for authorship.

Thank you for considering our manuscript. We look forward to your response.

Sincerely,

[Corresponding Author Name]
[Affiliation]
[Email]
[Phone]
"""

    cover_file = dest_dir / "cover_letter_template.md"
    with open(cover_file, 'w', encoding='utf-8') as f:
        f.write(cover_letter)

    print(f"  Created: {cover_file.name}")

# =============================================================================
# Step 6: Create Code Archive (Optional)
# =============================================================================

def create_code_archive(dest_dir: Path):
    """
    Create code repository for reproducibility

    Args:
        dest_dir: Destination directory
    """
    print("\n[CODE] Creating code archive...")

    # Key directories to include
    code_dirs = [
        BASE_DIR / "scripts",
        BASE_DIR / "src"
    ]

    code_files = [
        BASE_DIR / "MASTER_EXECUTE_ALL.py",
        BASE_DIR / "requirements.txt",
        BASE_DIR / "README.md",
        BASE_DIR / "COMPUTATIONAL_RESEARCH_ROADMAP.md"
    ]

    # Copy directories
    for src_dir in code_dirs:
        if src_dir.exists():
            dest = dest_dir / src_dir.name
            shutil.copytree(src_dir, dest, dirs_exist_ok=True)
            print(f"  Copied: {src_dir.name}/")

    # Copy files
    for src_file in code_files:
        if src_file.exists():
            dest = dest_dir / src_file.name
            shutil.copy2(src_file, dest)
            print(f"  Copied: {src_file.name}")

    # Create README
    code_readme = """# Code Repository

## Overview
This directory contains all code used to generate the results in the manuscript.

## Requirements
- Python 3.11+
- R 4.3+
- See requirements.txt for Python packages

## Execution
Run the complete pipeline:
```bash
python MASTER_EXECUTE_ALL.py
```

## Organization
- `scripts/data_pipeline/`: Data download and preprocessing
- `scripts/analysis/`: Core analysis scripts
- `scripts/figures/`: Figure generation
- `scripts/manuscript/`: Manuscript preparation

## Reproducibility
All analyses are fully reproducible. Raw data can be obtained from TCGA/GEO.

For questions, contact: [email]
"""

    readme_file = dest_dir / "README.md"
    with open(readme_file, 'w', encoding='utf-8') as f:
        f.write(code_readme)

    print(f"  Created: code README.md")

# =============================================================================
# Step 7: Create Submission Checklist
# =============================================================================

def create_submission_checklist(package_dir: Path):
    """
    Create submission checklist

    Args:
        package_dir: Package directory
    """
    print("\n[CHECKLIST] Creating submission checklist...")

    checklist = """# Submission Checklist

## Pre-Submission
- [ ] All analyses completed successfully
- [ ] Manuscript reviewed and proofread
- [ ] All figures generated at publication quality (300 DPI)
- [ ] Supplementary materials organized
- [ ] Cover letter completed
- [ ] Author contributions defined
- [ ] Conflicts of interest declared

## Required Files
- [ ] Main manuscript (PDF)
- [ ] Main figures (separate files, high-res)
- [ ] Supplementary materials (tables, figures, data)
- [ ] Cover letter
- [ ] Author agreement forms (if required)
- [ ] ICMJE forms (if required)

## Journal-Specific Requirements
- [ ] Word count within limits
- [ ] References formatted correctly
- [ ] Figure legends complete
- [ ] Abbreviations defined
- [ ] Ethics statement included (if applicable)
- [ ] Data availability statement included
- [ ] Code availability statement included

## Final Checks
- [ ] All co-authors approved submission
- [ ] All files named correctly
- [ ] No identifying information in blinded version (if required)
- [ ] Manuscript guidelines followed

## Submission
- [ ] Create account on journal submission system
- [ ] Upload all files
- [ ] Complete submission form
- [ ] Review and submit

## Post-Submission
- [ ] Archive submission package
- [ ] Track manuscript status
- [ ] Prepare for potential revisions
"""

    checklist_file = package_dir / "SUBMISSION_CHECKLIST.md"
    with open(checklist_file, 'w', encoding='utf-8') as f:
        f.write(checklist)

    print(f"  Created: {checklist_file.name}")

# =============================================================================
# Step 8: Create ZIP Archive
# =============================================================================

def create_zip_archive(package_dir: Path):
    """
    Create ZIP archive of submission package

    Args:
        package_dir: Package directory

    Returns:
        Path to ZIP file
    """
    print("\n[ZIP] Creating archive...")

    zip_path = OUTPUT_DIR / f"{package_dir.name}.zip"

    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file in package_dir.rglob("*"):
            if file.is_file():
                arcname = file.relative_to(package_dir.parent)
                zipf.write(file, arcname)

    size_mb = zip_path.stat().st_size / (1024 * 1024)
    print(f"  Created: {zip_path.name} ({size_mb:.2f} MB)")

    return zip_path

# =============================================================================
# Main Pipeline
# =============================================================================

def main():
    """
    Main execution pipeline
    """
    print("\n" + "="*80)
    print("SUBMISSION PACKAGE CREATION PIPELINE")
    print("="*80)

    # Step 1: Create structure
    package_dir, dirs = create_package_structure()

    # Step 2: Copy manuscript
    copy_manuscript_files(dirs['manuscript'])

    # Step 3: Copy figures
    copy_main_figures(dirs['figures'])

    # Step 4: Copy supplementary
    copy_supplementary_materials(dirs['supplementary'])

    # Step 5: Create cover letter
    create_cover_letter(dirs['cover'])

    # Step 6: Create code archive
    create_code_archive(dirs['code'])

    # Step 7: Create checklist
    create_submission_checklist(package_dir)

    # Step 8: Create ZIP
    zip_path = create_zip_archive(package_dir)

    # Summary
    print("\n" + "="*80)
    print("SUBMISSION PACKAGE COMPLETE")
    print("="*80)

    print(f"\nPackage location: {package_dir}")
    print(f"ZIP archive: {zip_path}")

    # File count
    n_files = len(list(package_dir.rglob("*")))
    print(f"\nTotal files in package: {n_files}")

    print("\n" + "="*80)
    print("READY FOR SUBMISSION")
    print("="*80)

    print("\nNext steps:")
    print("  1. Review submission checklist")
    print("  2. Complete cover letter with real data")
    print("  3. Get all co-author approvals")
    print("  4. Submit to target journal")

    print("\n" + "="*80)

if __name__ == "__main__":
    main()
