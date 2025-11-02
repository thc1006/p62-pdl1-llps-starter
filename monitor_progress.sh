#!/bin/bash
# Progress monitoring script for PD-L1 pipeline

echo "=========================================="
echo "PD-L1 Pipeline Progress Monitor"
echo "Time: $(date '+%Y-%m-%d %H:%M:%S')"
echo "=========================================="
echo ""

# Check if pipeline is running
if ps aux | grep "MASTER_EXECUTE_ALL.py" | grep -v grep > /dev/null; then
    echo "✅ Pipeline Status: RUNNING"
else
    echo "❌ Pipeline Status: NOT RUNNING"
fi
echo ""

# Check download progress
echo "📥 Data Download Progress:"
echo "-------------------------------------------"
for project in TCGA-LUAD TCGA-LUSC TCGA-SKCM; do
    if [ -d "data/tcga_raw/$project" ]; then
        files=$(find data/tcga_raw/$project -type f 2>/dev/null | wc -l)
        size=$(du -sh data/tcga_raw/$project 2>/dev/null | awk '{print $1}')
        echo "  $project: $files files, $size"
    else
        echo "  $project: Not started"
    fi
done
echo ""

# Check execution log
echo "📝 Latest Log Entries:"
echo "-------------------------------------------"
tail -10 outputs/execution_logs/master_execution_*.log 2>/dev/null | grep -E "\[PHASE\]|\[OK\]|\[FAIL\]" | tail -5
echo ""

# Check current phase
echo "🎯 Current Phase:"
echo "-------------------------------------------"
tail -20 outputs/execution_logs/master_execution_*.log 2>/dev/null | grep "\[PHASE\]" | tail -1
echo ""

echo "=========================================="
