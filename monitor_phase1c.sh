#!/bin/bash
# Phase 1C Progress Monitor

echo "=== Phase 1C Monitor Started at $(date +%H:%M:%S) ==="
echo ""

while true; do
    # Check if process still running
    if ! ps -p 253041 > /dev/null 2>&1; then
        echo ""
        echo "🎉 Phase 1C process completed!"
        echo ""

        # Check for output files
        if [ -f "outputs/tcga_full_cohort_real/expression_matrix_full_real.csv" ]; then
            echo "✅ Output file created:"
            ls -lh outputs/tcga_full_cohort_real/expression_matrix_full_real.csv
            echo ""
            echo "File size: $(du -h outputs/tcga_full_cohort_real/expression_matrix_full_real.csv | cut -f1)"
        fi

        # Show last log lines
        echo ""
        echo "📋 Last log entries:"
        tail -20 outputs/execution_logs/master_execution_20251102_152125.log

        break
    fi

    # Get process stats
    STATS=$(ps -p 253041 -o %cpu,%mem,etime --no-headers 2>/dev/null)
    CPU=$(echo $STATS | awk '{print $1}')
    MEM=$(echo $STATS | awk '{print $2}')
    TIME=$(echo $STATS | awk '{print $3}')

    echo "[$(date +%H:%M:%S)] CPU: ${CPU}% | Memory: ${MEM}% | Runtime: ${TIME}"

    # Check for output file creation
    if [ -f "outputs/tcga_full_cohort_real/expression_matrix_full_real.csv" ]; then
        SIZE=$(du -h outputs/tcga_full_cohort_real/expression_matrix_full_real.csv 2>/dev/null | cut -f1)
        echo "              Output file detected: ${SIZE}"
    fi

    sleep 30
done

echo ""
echo "=== Monitor Stopped at $(date +%H:%M:%S) ==="
