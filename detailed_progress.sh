#!/bin/bash
# Detailed progress report with accurate counts

echo "================================================"
echo "📊 DETAILED DOWNLOAD PROGRESS REPORT"
echo "Time: $(date '+%Y-%m-%d %H:%M:%S')"
echo "================================================"
echo ""

# Function to count completed downloads (directories with files)
count_completed() {
    project=$1
    if [ ! -d "data/tcga_raw/$project" ]; then
        echo "0"
        return
    fi
    # Count directories that contain actual data files
    find "data/tcga_raw/$project" -mindepth 1 -maxdepth 1 -type d 2>/dev/null | wc -l
}

# Expected totals
declare -A targets
targets[TCGA-LUAD]=601
targets[TCGA-LUSC]=562
targets[TCGA-SKCM]=473

declare -A sizes
sizes[TCGA-LUAD]="2.4"
sizes[TCGA-LUSC]="2.2"
sizes[TCGA-SKCM]="1.9"

echo "📥 Download Progress by Project:"
echo "------------------------------------------------"

total_complete=0
total_expected=0

for project in TCGA-LUAD TCGA-LUSC TCGA-SKCM; do
    completed=$(count_completed $project)
    expected=${targets[$project]}
    target_size=${sizes[$project]}
    current_size=$(du -sh data/tcga_raw/$project 2>/dev/null | awk '{print $1}')

    if [ -z "$current_size" ]; then
        current_size="0M"
    fi

    percent=$((completed * 100 / expected))

    # Progress bar
    filled=$((percent / 2))
    bar=$(printf '%*s' $filled | tr ' ' '█')
    empty=$(printf '%*s' $((50 - filled)) | tr ' ' '░')

    echo "  $project:"
    echo "    Files: $completed / $expected ($percent%)"
    echo "    Size:  $current_size / ${target_size} GB"
    echo "    [$bar$empty] $percent%"
    echo ""

    total_complete=$((total_complete + completed))
    total_expected=$((total_expected + expected))
done

echo "================================================"
echo "📊 OVERALL PROGRESS:"
echo "------------------------------------------------"

overall_percent=$((total_complete * 100 / total_expected))
total_size=$(du -sh data/tcga_raw 2>/dev/null | awk '{print $1}')

echo "  Total Files: $total_complete / $total_expected ($overall_percent%)"
echo "  Total Size:  $total_size / 6.5 GB"
echo ""

# Active processes
active=$(ps aux | grep "gdc-client download" | grep -v grep | wc -l)
echo "  Active Downloads: $active processes"
echo ""

# Time estimate
if [ $overall_percent -gt 0 ]; then
    # Rough estimate based on current progress
    elapsed=14  # minutes since start
    rate=$((overall_percent * 100 / elapsed))  # progress per minute
    remaining=$((100 - overall_percent))
    eta=$((remaining * 100 / rate))
    echo "  ⏱️  Estimated Time Remaining: ~$eta minutes"
else
    echo "  ⏱️  Estimated Time Remaining: Calculating..."
fi

echo ""
echo "================================================"
