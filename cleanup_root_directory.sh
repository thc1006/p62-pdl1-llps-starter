#!/bin/bash
# 根目錄徹底清理腳本
# 目標：保持根目錄乾淨、專業、易於維護

PROJECT_ROOT="/home/thc1006/dev/p62-pdl1-llps-starter"
cd "$PROJECT_ROOT" || exit 1

echo "=========================================="
echo "開始根目錄徹底清理..."
echo "=========================================="
echo ""

# 1. 創建必要的目錄結構
echo "[1/8] 創建整理目錄..."
mkdir -p logs/execution
mkdir -p logs/timer2
mkdir -p logs/r_installation
mkdir -p logs/monitoring
mkdir -p docs/reports
mkdir -p docs/guides
mkdir -p archive/old_scripts
mkdir -p archive/old_reports
echo "  ✓ 目錄結構已建立"
echo ""

# 2. 移動所有 .log 文件到 logs/
echo "[2/8] 整理 .log 文件..."

# 執行相關的 log
mv -f execution*.log logs/execution/ 2>/dev/null
mv -f phase_*.log logs/execution/ 2>/dev/null
mv -f pipeline_*.log logs/execution/ 2>/dev/null

# TIMER2 相關的 log
mv -f timer2*.log logs/timer2/ 2>/dev/null

# R 安裝相關的 log
mv -f r_package*.log logs/r_installation/ 2>/dev/null
mv -f iobr*.log logs/r_installation/ 2>/dev/null
mv -f *_deps*.log logs/r_installation/ 2>/dev/null
mv -f *install*.log logs/r_installation/ 2>/dev/null

# 監控和其他 log
mv -f *monitor*.log logs/monitoring/ 2>/dev/null
mv -f automation*.log logs/execution/ 2>/dev/null
mv -f enrichment*.log logs/execution/ 2>/dev/null
mv -f pdf*.log logs/execution/ 2>/dev/null
mv -f figure_generation*.log logs/execution/ 2>/dev/null

LOG_COUNT=$(ls -1 logs/execution/*.log 2>/dev/null | wc -l)
echo "  ✓ 已整理 $LOG_COUNT 個 log 文件到 logs/ 目錄"
echo ""

# 3. 整理文檔和報告
echo "[3/8] 整理文檔和報告..."

# 移動報告類文件到 docs/reports/
mv -f *_REPORT.md docs/reports/ 2>/dev/null
mv -f AUTOMATION_SUMMARY.json docs/reports/ 2>/dev/null
mv -f WAKE_UP_GUIDE.txt docs/reports/ 2>/dev/null

# 移動指南類文件到 docs/guides/
mv -f *_GUIDE.md docs/guides/ 2>/dev/null
mv -f QUICK_START.md docs/guides/ 2>/dev/null
mv -f 00_START_HERE.txt docs/guides/ 2>/dev/null

# 移動其他文檔
mv -f NEXT_STEPS.md docs/ 2>/dev/null
mv -f PROJECT_STATUS.md docs/ 2>/dev/null
mv -f PROJECT_PROGRESS.md docs/ 2>/dev/null
mv -f REVISION_SUMMARY.md docs/ 2>/dev/null
mv -f COMPUTATIONAL_RESEARCH_ROADMAP.md docs/ 2>/dev/null
mv -f COMPUTATIONAL_ANALYSIS_DISCLAIMER.md docs/ 2>/dev/null
mv -f NATURE_ENHANCEMENT_STARTED.txt docs/ 2>/dev/null

DOC_COUNT=$(find docs/reports docs/guides -type f 2>/dev/null | wc -l)
echo "  ✓ 已整理 $DOC_COUNT 個文檔到 docs/ 目錄"
echo ""

# 4. 移動舊腳本到 archive/
echo "[4/8] 歸檔舊腳本..."

# 移動臨時腳本
mv -f install_*.R archive/old_scripts/ 2>/dev/null
mv -f monitor_*.sh archive/old_scripts/ 2>/dev/null
mv -f generate_pdf.py archive/old_scripts/ 2>/dev/null
mv -f AUTOMATED_MANUSCRIPT_FINALIZATION.py archive/old_scripts/ 2>/dev/null

SCRIPT_COUNT=$(ls -1 archive/old_scripts/ 2>/dev/null | wc -l)
echo "  ✓ 已歸檔 $SCRIPT_COUNT 個舊腳本"
echo ""

# 5. 保留核心投稿材料在根目錄
echo "[5/8] 確認核心投稿材料..."
CORE_FILES=(
    "MANUSCRIPT_bioRxiv_SUBMISSION.pdf"
    "BIORXIV_SUBMISSION_GUIDE.md"
    "SUBMISSION_MATERIALS_COMPLETE.md"
    "SUPPLEMENTARY_MATERIALS.md"
)

for file in "${CORE_FILES[@]}"; do
    if [ -f "$file" ]; then
        echo "  ✓ $file (已保留)"
    fi
done
echo ""

# 6. 保留核心項目文件
echo "[6/8] 確認核心項目文件..."
PROJECT_FILES=(
    "README.md"
    "LICENSE"
    "requirements.txt"
    "Dockerfile"
    "docker-compose.yml"
    "Makefile"
    "MASTER_EXECUTE_ALL.py"
    "cleanup_project.sh"
)

for file in "${PROJECT_FILES[@]}"; do
    if [ -f "$file" ]; then
        echo "  ✓ $file"
    fi
done
echo ""

# 7. 列出根目錄當前狀態
echo "[7/8] 根目錄整理後狀態："
echo ""
ls -lh | grep -v '^d' | grep -v '^total' | awk '{print "  " $9 " (" $5 ")"}'
echo ""

# 8. 統計報告
echo "[8/8] 整理統計報告："
echo ""
echo "  📁 目錄結構："
echo "     - logs/         : $(find logs -type f 2>/dev/null | wc -l) 個日誌文件"
echo "     - docs/         : $(find docs -type f 2>/dev/null | wc -l) 個文檔"
echo "     - archive/      : $(find archive -type f 2>/dev/null | wc -l) 個歸檔文件"
echo "     - scripts/      : $(find scripts -type f 2>/dev/null | wc -l) 個腳本"
echo "     - outputs/      : $(find outputs -type f 2>/dev/null | wc -l) 個輸出文件"
echo ""
echo "  📄 根目錄文件數："
ROOT_FILE_COUNT=$(ls -1 | grep -v '^d' | wc -l)
echo "     - 總計: $ROOT_FILE_COUNT 個文件"
echo ""

# 9. 專案大小統計
echo "  💾 專案大小："
du -sh "$PROJECT_ROOT" 2>/dev/null | awk '{print "     - 總大小: " $1}'
du -sh logs/ 2>/dev/null | awk '{print "     - logs/:   " $1}'
du -sh outputs/ 2>/dev/null | awk '{print "     - outputs/: " $1}'
du -sh data/ 2>/dev/null | awk '{print "     - data/:   " $1}'
echo ""

echo "=========================================="
echo "✅ 根目錄清理完成！"
echo "=========================================="
echo ""
echo "根目錄現在只保留："
echo "  1. 核心投稿材料 (MANUSCRIPT, BIORXIV_GUIDE, etc.)"
echo "  2. 核心項目文件 (README, requirements.txt, etc.)"
echo "  3. 主要執行腳本 (MASTER_EXECUTE_ALL.py)"
echo ""
echo "所有日誌、報告、舊腳本已整理到相應目錄。"
echo ""
