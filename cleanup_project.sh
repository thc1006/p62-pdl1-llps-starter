#!/bin/bash
# 專案清理腳本 - 確保結構清晰、整潔、乾淨
# 執行日期: 2025-11-06

PROJECT_ROOT="/home/thc1006/dev/p62-pdl1-llps-starter"

echo "=================================="
echo "開始專案清理..."
echo "=================================="
echo ""

# 記錄清理前的大小
echo "📊 清理前專案大小："
du -sh "$PROJECT_ROOT" 2>/dev/null
echo ""

# 1. 刪除 paper/archive/ 中的舊版論文
echo "[1/9] 清理 paper/archive/..."
if [ -d "$PROJECT_ROOT/paper/archive" ]; then
    rm -rf "$PROJECT_ROOT/paper/archive/"
    echo "  ✓ 已刪除 paper/archive/ 目錄"
else
    echo "  ℹ paper/archive/ 不存在"
fi

# 2. 刪除重複的論文檔案
echo "[2/9] 刪除重複論文檔案..."
rm -f "$PROJECT_ROOT/paper/manuscript_v2.md" 2>/dev/null && echo "  ✓ 已刪除 manuscript_v2.md"
rm -f "$PROJECT_ROOT/paper/manuscript_v2_optimized.pdf" 2>/dev/null && echo "  ✓ 已刪除 manuscript_v2_optimized.pdf"

# 3. 刪除備份腳本
echo "[3/9] 刪除備份腳本..."
rm -f "$PROJECT_ROOT/scripts/data_pipeline/02_process_expression.py.backup" 2>/dev/null && echo "  ✓ 已刪除 .backup 檔案"

# 4. 清理 Python 快取
echo "[4/9] 清理 Python 快取..."
rm -rf "$PROJECT_ROOT/__pycache__" 2>/dev/null && echo "  ✓ 已刪除 __pycache__"
# 清理所有 __pycache__ (但保留 venv)
find "$PROJECT_ROOT" -type d -name "__pycache__" ! -path "*/venv/*" -exec rm -rf {} + 2>/dev/null
echo "  ✓ 已清理所有 Python 快取"

# 5. 清理舊執行日誌 (保留最新 2 個)
echo "[5/9] 清理舊執行日誌..."
if [ -d "$PROJECT_ROOT/outputs/execution_logs/" ]; then
    cd "$PROJECT_ROOT/outputs/execution_logs/"
    # 保留最新 2 個 .log 檔案
    ls -t master_execution_*.log 2>/dev/null | tail -n +3 | xargs rm -f 2>/dev/null
    # 保留最新 2 個 .json 檔案
    ls -t execution_report_*.json 2>/dev/null | tail -n +3 | xargs rm -f 2>/dev/null
    echo "  ✓ 已清理舊執行日誌（保留最新 2 個）"
    cd "$PROJECT_ROOT"
fi

# 6. 刪除過渡進度報告
echo "[6/9] 清理過渡進度報告..."
rm -f "$PROJECT_ROOT/docs/progress_reports/PROGRESS_14_12.md" 2>/dev/null
rm -f "$PROJECT_ROOT/docs/progress_reports/PROGRESS_14_15.md" 2>/dev/null
rm -f "$PROJECT_ROOT/docs/progress_reports/PROGRESS_14_28.md" 2>/dev/null
rm -f "$PROJECT_ROOT/docs/progress_reports/PROGRESS_14_37.md" 2>/dev/null
rm -f "$PROJECT_ROOT/docs/progress_reports/PROGRESS_14_56.md" 2>/dev/null
rm -f "$PROJECT_ROOT/docs/progress_reports/PROGRESS_15_12.md" 2>/dev/null
echo "  ✓ 已刪除過渡進度報告（保留里程碑報告）"

# 7. 刪除過時狀態報告
echo "[7/9] 清理過時狀態報告..."
rm -f "$PROJECT_ROOT/docs/status_reports/current_status.md" 2>/dev/null
rm -f "$PROJECT_ROOT/docs/status_reports/COMPLETE_STATUS.md" 2>/dev/null
rm -f "$PROJECT_ROOT/docs/status_reports/EXPLORATION_SUMMARY.txt" 2>/dev/null
echo "  ✓ 已刪除過時狀態報告"

# 8. 清理 .pyc 檔案
echo "[8/9] 清理 .pyc 檔案..."
find "$PROJECT_ROOT" -type f -name "*.pyc" ! -path "*/venv/*" -delete 2>/dev/null
echo "  ✓ 已清理所有 .pyc 檔案"

# 9. 清理空目錄
echo "[9/9] 清理空目錄..."
find "$PROJECT_ROOT" -type d -empty ! -path "*/venv/*" ! -path "*/.git/*" -delete 2>/dev/null
echo "  ✓ 已清理空目錄"

echo ""
echo "=================================="
echo "清理完成！"
echo "=================================="
echo ""

# 記錄清理後的大小
echo "📊 清理後專案大小："
du -sh "$PROJECT_ROOT" 2>/dev/null
echo ""

echo "✅ 專案結構現已清晰、整潔、乾淨！"
echo ""
echo "📝 下一步："
echo "   1. 執行 git status 查看變更"
echo "   2. 執行 git add . && git commit -m 'Clean up project structure'"
echo "   3. 查看 BIORXIV_SUBMISSION_GUIDE.md 了解投稿材料"
