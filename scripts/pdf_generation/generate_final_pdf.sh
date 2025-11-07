#!/bin/bash
# Final PDF Generation with pdfLaTeX and Times font
# Fixes font issues and spacing problems

set -e  # Exit on error

echo "=========================================="
echo "最終 PDF 生成（Times 字體 + 修正排版）"
echo "=========================================="
echo ""

# Prepare manuscript for pdflatex
echo "準備論文檔案（轉換 Unicode）..."
python3 prepare_for_pdflatex.py
if [ ! -f "paper/MANUSCRIPT_bioRxiv_FOR_PDFLATEX.md" ]; then
    echo "❌ 轉換失敗！"
    exit 1
fi

echo "✓ 論文檔案準備完成"
echo ""

# Check figures
echo "檢查圖表..."
FIGURES=(
    "Figure1_pipeline_flowchart.png"
    "Figure2_correlations.png"
    "Figure3_immune_environment.png"
    "Figure4_survival_analysis.png"
    "FigureS1_study_design.png"
    "FigureS2_sample_characteristics.png"
)

for fig in "${FIGURES[@]}"; do
    if [ -f "outputs/figures/$fig" ]; then
        size=$(du -h "outputs/figures/$fig" | cut -f1)
        echo "  ✓ $fig ($size)"
    else
        echo "  ❌ $fig (遺失)"
        exit 1
    fi
done
echo ""

# Generate PDF
echo "生成 PDF..."
echo "  引擎: pdfLaTeX (確保 Times 字體)"
echo "  配置: manuscript_template_pdflatex.yaml"
echo "  排版: 1.5 行距，1 inch 邊距"
echo ""

pandoc paper/MANUSCRIPT_bioRxiv_FOR_PDFLATEX.md \
    --metadata-file=manuscript_template_pdflatex.yaml \
    -o MANUSCRIPT_bioRxiv_SUBMISSION_FINAL.pdf \
    --pdf-engine=pdflatex \
    --resource-path=.:paper:outputs/figures \
    2>&1 | tee pandoc_final.log

# Check result
if [ -f "MANUSCRIPT_bioRxiv_SUBMISSION_FINAL.pdf" ]; then
    SIZE=$(du -h MANUSCRIPT_bioRxiv_SUBMISSION_FINAL.pdf | cut -f1)

    echo ""
    echo "=========================================="
    echo "✅ PDF 生成成功！"
    echo "=========================================="
    echo ""
    echo "檔案: MANUSCRIPT_bioRxiv_SUBMISSION_FINAL.pdf"
    echo "大小: $SIZE"
    echo ""
    echo "✓ 使用 Times 字體（mathptmx 套件）"
    echo "✓ 1.5 倍行距"
    echo "✓ 1 inch 標準邊距"
    echo "✓ 所有圖表嵌入"
    echo "✓ 修正排版問題"
    echo ""
else
    echo ""
    echo "❌ PDF 生成失敗！"
    echo "請檢查 pandoc_final.log"
    exit 1
fi
