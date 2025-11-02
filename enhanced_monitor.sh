#!/bin/bash
# Enhanced progress monitor for parallel downloads

echo "=========================================="
echo "🚀 PARALLEL DOWNLOAD PROGRESS"
echo "Time: $(date '+%Y-%m-%d %H:%M:%S')"
echo "=========================================="
echo ""

# Download progress
echo "📥 Data Download Progress (Parallel):"
echo "-------------------------------------------"
for project in TCGA-LUAD TCGA-LUSC TCGA-SKCM; do
    if [ -d "data/tcga_raw/$project" ]; then
        files=$(find data/tcga_raw/$project -type f -name "*.gz" 2>/dev/null | wc -l)
        size=$(du -sh data/tcga_raw/$project 2>/dev/null | awk '{print $1}')

        # Expected totals
        case $project in
            TCGA-LUAD) total="601 files, ~2.4 GB" ;;
            TCGA-LUSC) total="562 files, ~2.2 GB" ;;
            TCGA-SKCM) total="473 files, ~1.9 GB" ;;
        esac

        echo "  ✓ $project: $files files, $size (Target: $total)"
    else
        echo "  ✗ $project: Not started"
    fi
done
echo ""

# Active processes
active=$(ps aux | grep "gdc-client download" | grep -v grep | wc -l)
echo "🔧 Active Downloads: $active processes"
echo ""

# Total progress
total_size=$(du -sh data/tcga_raw 2>/dev/null | awk '{print $1}')
echo "📊 Total Downloaded: $total_size / ~6.5 GB"
echo ""

# Estimated completion
echo "⏱️  Estimated Time to Complete:"
echo "   With parallel download: ~20-30 minutes remaining"
echo ""

echo "=========================================="
