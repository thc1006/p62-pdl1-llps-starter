#!/bin/bash
# Automatic progress monitoring with milestone detection

MILESTONE_FILE="/tmp/pipeline_milestone.txt"
LOG_FILE="outputs/execution_logs/master_execution_*.log"

# Initialize milestone if doesn't exist
if [ ! -f "$MILESTONE_FILE" ]; then
    echo "PHASE_1A" > $MILESTONE_FILE
fi

LAST_MILESTONE=$(cat $MILESTONE_FILE)

# Check current status
CURRENT_PHASE=$(tail -50 $LOG_FILE 2>/dev/null | grep "\[PHASE\]" | tail -1 | awk '{print $4}')

# Detect phase completion
COMPLETED=$(tail -50 $LOG_FILE 2>/dev/null | grep "\[OK\]" | tail -1)

echo "=== Auto Monitor [$(date '+%H:%M:%S')] ==="
echo "Last Milestone: $LAST_MILESTONE"
echo "Current Phase: $CURRENT_PHASE"

# Check for milestones
if [ "$CURRENT_PHASE" != "" ] && [ "$CURRENT_PHASE" != "$LAST_MILESTONE" ]; then
    echo "🎉 MILESTONE: Moved from $LAST_MILESTONE to $CURRENT_PHASE"
    echo "$CURRENT_PHASE" > $MILESTONE_FILE

    # Show detailed progress
    bash monitor_progress.sh
fi

# Check download progress
LUAD_SIZE=$(du -sm data/tcga_raw/TCGA-LUAD 2>/dev/null | awk '{print $1}')
LUSC_SIZE=$(du -sm data/tcga_raw/TCGA-LUSC 2>/dev/null | awk '{print $1}')
SKCM_SIZE=$(du -sm data/tcga_raw/TCGA-SKCM 2>/dev/null | awk '{print $1}')

echo "Download Status: LUAD=${LUAD_SIZE}MB LUSC=${LUSC_SIZE}MB SKCM=${SKCM_SIZE}MB"

# Check for completion
if grep -q "EXECUTION COMPLETE" $LOG_FILE 2>/dev/null; then
    echo "🎉🎉🎉 PIPELINE COMPLETED! 🎉🎉🎉"
    bash monitor_progress.sh
    exit 0
fi

# Check for errors
if tail -20 $LOG_FILE 2>/dev/null | grep -q "\[FAIL\]"; then
    echo "❌ ERROR DETECTED in pipeline"
    tail -30 $LOG_FILE
    exit 1
fi

echo "=== Monitor OK ==="
