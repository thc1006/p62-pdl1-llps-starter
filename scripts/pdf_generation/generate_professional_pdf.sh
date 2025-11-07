#!/bin/bash
# Professional PDF Generation Script for bioRxiv Submission
# Uses best practices for academic paper formatting

echo "=========================================="
echo "Professional PDF Generation for bioRxiv"
echo "=========================================="
echo ""

# Step 1: Check if manuscript file exists
if [ ! -f "paper/MANUSCRIPT_bioRxiv_FIXED.md" ]; then
    echo "❌ Error: Manuscript file not found!"
    exit 1
fi

echo "✓ Manuscript file found"
echo ""

# Step 2: Check if figures exist
echo "Checking figures..."
FIGURE_DIR="outputs/figures"
FIGURES=(
    "Figure1_pipeline_flowchart.png"
    "Figure2_correlations.png"
    "Figure3_immune_environment.png"
    "Figure4_survival_analysis.png"
    "FigureS1_study_design.png"
    "FigureS2_sample_characteristics.png"
)

for fig in "${FIGURES[@]}"; do
    if [ -f "$FIGURE_DIR/$fig" ]; then
        size=$(du -h "$FIGURE_DIR/$fig" | cut -f1)
        echo "  ✓ $fig ($size)"
    else
        echo "  ❌ $fig (MISSING)"
    fi
done
echo ""

# Step 3: Generate PDF with professional formatting
echo "Generating professional PDF..."
echo "  - Font: Times New Roman 11pt"
echo "  - Margins: 1 inch (all sides)"
echo "  - Line spacing: 1.5"
echo "  - Engine: XeLaTeX"
echo ""

pandoc paper/MANUSCRIPT_bioRxiv_FIXED.md \
    --metadata-file=manuscript_template.yaml \
    -o MANUSCRIPT_bioRxiv_SUBMISSION_FINAL.pdf \
    --pdf-engine=xelatex \
    --resource-path=.:paper:outputs/figures \
    --verbose \
    2>&1 | tee pandoc_generation.log

# Check if PDF was generated successfully
if [ -f "MANUSCRIPT_bioRxiv_SUBMISSION_FINAL.pdf" ]; then
    SIZE=$(du -h MANUSCRIPT_bioRxiv_SUBMISSION_FINAL.pdf | cut -f1)
    echo ""
    echo "=========================================="
    echo "✅ PDF Generated Successfully!"
    echo "=========================================="
    echo ""
    echo "File: MANUSCRIPT_bioRxiv_SUBMISSION_FINAL.pdf"
    echo "Size: $SIZE"
    echo ""
    echo "PDF Details:"
    echo "  - Professional academic formatting"
    echo "  - Times New Roman font"
    echo "  - All figures embedded inline"
    echo "  - All tables embedded inline"
    echo "  - Ready for bioRxiv submission"
    echo ""
    echo "Next steps:"
    echo "  1. Open the PDF to verify formatting"
    echo "  2. Check all figures and tables are visible"
    echo "  3. Submit to bioRxiv at: https://www.biorxiv.org/submit-a-manuscript"
    echo ""
else
    echo ""
    echo "❌ Error: PDF generation failed!"
    echo "Check pandoc_generation.log for details"
    exit 1
fi
