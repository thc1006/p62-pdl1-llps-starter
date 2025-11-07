#!/bin/bash
# 專案清理腳本 - 準備公開發布
# 將檔案整理為清晰的結構

set -e

echo "=========================================="
echo "專案檔案結構清理"
echo "=========================================="
echo ""

# 創建目錄結構
echo "創建目錄結構..."
mkdir -p scripts/figure_generation/tikz
mkdir -p scripts/pdf_generation
mkdir -p docs/reports
mkdir -p docs/development
mkdir -p temp_files

# ==================== 移動 TikZ 相關檔案 ====================
echo "整理 TikZ 檔案..."
if [ -f "figure1_tikz.tex" ]; then
    mv figure1_tikz.tex scripts/figure_generation/tikz/
    echo "  ✓ figure1_tikz.tex → scripts/figure_generation/tikz/"
fi
if [ -f "figure1_tikz.pdf" ]; then
    mv figure1_tikz.pdf scripts/figure_generation/tikz/
    echo "  ✓ figure1_tikz.pdf → scripts/figure_generation/tikz/"
fi

# ==================== 移動生成腳本 ====================
echo "整理生成腳本..."
SCRIPTS=(
    "generate_manuscript_figures.py"
    "generate_manuscript_figures_fixed.py"
    "redesign_figures.py"
)
for script in "${SCRIPTS[@]}"; do
    if [ -f "$script" ]; then
        mv "$script" scripts/figure_generation/
        echo "  ✓ $script → scripts/figure_generation/"
    fi
done

PDF_SCRIPTS=(
    "generate_final_pdf.sh"
    "generate_professional_pdf.sh"
    "prepare_for_pdflatex.py"
)
for script in "${PDF_SCRIPTS[@]}"; do
    if [ -f "$script" ]; then
        mv "$script" scripts/pdf_generation/
        echo "  ✓ $script → scripts/pdf_generation/"
    fi
done

# ==================== 移動報告文件 ====================
echo "整理報告文件..."
REPORTS=(
    "FINAL_IMPROVEMENTS_REPORT.md"
    "PROFESSIONAL_PDF_IMPROVEMENTS.md"
    "PROJECT_CLEANUP_REPORT.md"
    "CLEANUP_SUMMARY.txt"
)
for report in "${REPORTS[@]}"; do
    if [ -f "$report" ]; then
        mv "$report" docs/reports/
        echo "  ✓ $report → docs/reports/"
    fi
done

# ==================== 移動開發文件 ====================
echo "整理開發文件..."
DEV_DOCS=(
    "FINAL_PERFECT_SUBMISSION.md"
    "SUBMISSION_MATERIALS_COMPLETE.md"
)
for doc in "${DEV_DOCS[@]}"; do
    if [ -f "$doc" ]; then
        mv "$doc" docs/development/
        echo "  ✓ $doc → docs/development/"
    fi
done

# ==================== 移動配置檔案 ====================
echo "整理配置檔案..."
CONFIG_DIR="config"
mkdir -p $CONFIG_DIR
CONFIGS=(
    "manuscript_template.yaml"
    "manuscript_template_pdflatex.yaml"
)
for config in "${CONFIGS[@]}"; do
    if [ -f "$config" ]; then
        mv "$config" $CONFIG_DIR/
        echo "  ✓ $config → $CONFIG_DIR/"
    fi
done

# ==================== 移動舊版 PDF ====================
echo "整理 PDF 檔案..."
if [ -f "MANUSCRIPT_bioRxiv_SUBMISSION_FINAL_NEW.pdf" ]; then
    mv MANUSCRIPT_bioRxiv_SUBMISSION_FINAL_NEW.pdf archive/old_pdfs/
    echo "  ✓ 舊版 PDF → archive/old_pdfs/"
fi

# ==================== 清理臨時檔案 ====================
echo "清理臨時檔案..."
TEMP_FILES=(
    "figure1_tikz.aux"
    "figure1_tikz.log"
    "missfont.log"
    "pandoc_final.log"
    "pandoc_generation.log"
    "pandoc_output.log"
)
for temp in "${TEMP_FILES[@]}"; do
    if [ -f "$temp" ]; then
        mv "$temp" temp_files/
        echo "  ✓ $temp → temp_files/"
    fi
done

# ==================== 移動舊清理腳本 ====================
echo "整理清理腳本..."
if [ -f "cleanup_project.sh" ]; then
    mv cleanup_project.sh archive/
    echo "  ✓ cleanup_project.sh → archive/"
fi
if [ -f "cleanup_root_directory.sh" ]; then
    mv cleanup_root_directory.sh archive/
    echo "  ✓ cleanup_root_directory.sh → archive/"
fi

echo ""
echo "=========================================="
echo "✅ 清理完成！"
echo "=========================================="
echo ""

# 顯示清理後的根目錄
echo "根目錄檔案（僅核心檔案）:"
ls -1 | grep -v "^archive$\|^docs$\|^outputs$\|^paper$\|^scripts$\|^temp_files$\|^config$\|^logs$\|^docker$\|^mcp$\|^protocols$\|^scripts_generated$\|^skills$\|^tools$\|^workflows$" || true

echo ""
echo "目錄結構："
tree -L 2 -d --charset ascii 2>/dev/null || ls -d */ 2>/dev/null || echo "  (使用 ls 查看)"
