#!/usr/bin/env python3
"""
Generate PDF from Manuscript Markdown
Converts updated manuscript to publication-ready PDF

Uses: pandoc for markdown to PDF conversion

Author: Automated Pipeline
Date: 2025-11-02
"""

import subprocess
from pathlib import Path
import sys

# =============================================================================
# Configuration
# =============================================================================

BASE_DIR = Path(__file__).parent.parent.parent
MANUSCRIPT_DIR = BASE_DIR / "paper"
FIGURES_DIR = BASE_DIR / "outputs" / "figures_publication"

INPUT_FILE = MANUSCRIPT_DIR / "manuscript_updated.md"
OUTPUT_FILE = MANUSCRIPT_DIR / "manuscript_final.pdf"

# Pandoc template
PANDOC_TEMPLATE = """
---
title: "Systematic Multi-Level Validation of PD-L1 Regulatory Network in Cancer"
author:
  - "Computational Research Team"
date: "2025-11-02"
geometry: margin=1in
fontsize: 11pt
linestretch: 1.5
numbersections: true
---
"""

# =============================================================================
# Step 1: Check Dependencies
# =============================================================================

def check_pandoc():
    """
    Check if pandoc is installed

    Returns:
        True if pandoc available
    """
    print("\n[CHECK] Verifying pandoc installation...")

    try:
        result = subprocess.run(
            ["pandoc", "--version"],
            capture_output=True,
            text=True,
            check=True
        )

        version = result.stdout.split('\n')[0]
        print(f"  Found: {version}")
        return True

    except (subprocess.CalledProcessError, FileNotFoundError):
        print("\n[ERROR] pandoc not found!")
        print("\nInstallation instructions:")
        print("  Windows: choco install pandoc")
        print("  Or download from: https://pandoc.org/installing.html")
        print("\nAlternative: Install MiKTeX or TeX Live for LaTeX support")
        return False

# =============================================================================
# Step 2: Prepare Manuscript
# =============================================================================

def prepare_manuscript() -> Path:
    """
    Prepare manuscript with YAML front matter

    Returns:
        Path to prepared manuscript
    """
    print("\n[PREPARE] Adding metadata to manuscript...")

    if not INPUT_FILE.exists():
        print(f"\n[ERROR] Manuscript not found: {INPUT_FILE}")
        print("  Please run: python scripts/manuscript/update_manuscript.py")
        sys.exit(1)

    # Read manuscript
    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        content = f.read()

    # Prepend YAML metadata
    full_content = PANDOC_TEMPLATE + "\n" + content

    # Save prepared version
    prepared_file = MANUSCRIPT_DIR / "manuscript_prepared.md"
    with open(prepared_file, 'w', encoding='utf-8') as f:
        f.write(full_content)

    print(f"  Saved: {prepared_file}")

    return prepared_file

# =============================================================================
# Step 3: Convert to PDF
# =============================================================================

def convert_to_pdf(input_file: Path, output_file: Path) -> bool:
    """
    Convert markdown to PDF using pandoc

    Args:
        input_file: Input markdown file
        output_file: Output PDF file

    Returns:
        Success status
    """
    print(f"\n[CONVERT] Generating PDF...")
    print(f"  Input: {input_file}")
    print(f"  Output: {output_file}")

    # Pandoc command
    cmd = [
        "pandoc",
        str(input_file),
        "-o", str(output_file),
        "--pdf-engine=xelatex",  # Use XeLaTeX for better Unicode support
        "--toc",  # Table of contents
        "--number-sections",  # Number sections
        "--highlight-style=tango",  # Code highlighting
        "-V", "documentclass=article",
        "-V", "geometry:margin=1in",
        "-V", "fontsize=11pt",
        "-V", "linestretch=1.5"
    ]

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True,
            timeout=120
        )

        if output_file.exists():
            size_mb = output_file.stat().st_size / (1024 * 1024)
            print(f"\n[SUCCESS] PDF generated ({size_mb:.2f} MB)")
            return True
        else:
            print("\n[ERROR] PDF file not created")
            return False

    except subprocess.TimeoutExpired:
        print("\n[ERROR] PDF conversion timed out")
        return False

    except subprocess.CalledProcessError as e:
        print(f"\n[ERROR] Pandoc failed:")
        print(e.stderr)

        # Suggest fallback
        print("\n[FALLBACK] Trying simple PDF conversion...")

        # Simpler command without advanced features
        cmd_simple = [
            "pandoc",
            str(input_file),
            "-o", str(output_file)
        ]

        try:
            subprocess.run(cmd_simple, check=True, timeout=60)
            if output_file.exists():
                print(f"\n[SUCCESS] Simple PDF generated")
                return True
        except:
            print("\n[ERROR] Simple conversion also failed")

        return False

    except FileNotFoundError:
        print("\n[ERROR] pandoc not found in PATH")
        return False

# =============================================================================
# Step 4: Create HTML Version (Fallback)
# =============================================================================

def convert_to_html(input_file: Path) -> bool:
    """
    Create HTML version as fallback

    Args:
        input_file: Input markdown file

    Returns:
        Success status
    """
    print("\n[FALLBACK] Generating HTML version...")

    output_html = MANUSCRIPT_DIR / "manuscript_final.html"

    cmd = [
        "pandoc",
        str(input_file),
        "-o", str(output_html),
        "--standalone",
        "--toc",
        "--css=https://cdn.jsdelivr.net/npm/water.css@2/out/water.css"
    ]

    try:
        subprocess.run(cmd, check=True, timeout=60)

        if output_html.exists():
            print(f"  [SUCCESS] HTML version: {output_html}")
            return True

        return False

    except Exception as e:
        print(f"  [ERROR] HTML conversion failed: {e}")
        return False

# =============================================================================
# Main Pipeline
# =============================================================================

def main():
    """
    Main execution pipeline
    """
    print("\n" + "="*80)
    print("MANUSCRIPT PDF GENERATION PIPELINE")
    print("="*80)

    # Step 1: Check dependencies
    has_pandoc = check_pandoc()

    if not has_pandoc:
        print("\n[SKIP] Cannot generate PDF without pandoc")
        print("  Manuscript text available at: {INPUT_FILE}")
        sys.exit(1)

    # Step 2: Prepare manuscript
    prepared_file = prepare_manuscript()

    # Step 3: Convert to PDF
    success = convert_to_pdf(prepared_file, OUTPUT_FILE)

    # Step 4: Fallback to HTML if PDF fails
    if not success:
        print("\n[WARNING] PDF generation failed, creating HTML version...")
        convert_to_html(prepared_file)

    # Summary
    print("\n" + "="*80)
    print("PDF GENERATION COMPLETE")
    print("="*80)

    if success:
        print(f"\nFinal PDF: {OUTPUT_FILE}")
        print(f"  Open with: start {OUTPUT_FILE}")  # Windows
    else:
        print(f"\nPDF generation unsuccessful")
        print(f"  HTML version available at: {MANUSCRIPT_DIR / 'manuscript_final.html'}")
        print(f"  Markdown version at: {INPUT_FILE}")

    print("\n" + "="*80)
    print("Next step:")
    print("  Run: python scripts/submission/prepare_supplementary.py")
    print("="*80)

if __name__ == "__main__":
    main()
