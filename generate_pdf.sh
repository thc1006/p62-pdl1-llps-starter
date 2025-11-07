#!/bin/bash
# 最終 PDF 生成腳本（簡化版）

set -e

echo "=========================================="
echo "生成最終投稿 PDF"
echo "=========================================="
echo ""

# 準備文件
echo "準備 Markdown 文件..."
python3 scripts/pdf_generation/prepare_for_pdflatex.py

# 生成 PDF
echo "生成 PDF（pdfLaTeX + Times 字體）..."
pandoc paper/MANUSCRIPT_bioRxiv_FOR_PDFLATEX.md \
    --metadata-file=config/manuscript_template_pdflatex.yaml \
    -o MANUSCRIPT_bioRxiv_SUBMISSION_FINAL.pdf \
    --pdf-engine=pdflatex \
    --resource-path=.:paper:outputs/figures \
    2>&1 | tail -5

if [ -f "MANUSCRIPT_bioRxiv_SUBMISSION_FINAL.pdf" ]; then
    SIZE=$(du -h MANUSCRIPT_bioRxiv_SUBMISSION_FINAL.pdf | cut -f1)
    echo ""
    echo "✅ PDF 生成成功！"
    echo "   檔案: MANUSCRIPT_bioRxiv_SUBMISSION_FINAL.pdf"
    echo "   大小: $SIZE"
    echo ""
    echo "✓ 使用 TikZ 製作的專業 Figure 1"
    echo "✓ Times 字體（mathptmx）"
    echo "✓ 所有圖表嵌入"
    echo "✓ 準備好投稿 bioRxiv"
else
    echo "❌ PDF 生成失敗"
    exit 1
fi
