#!/bin/bash
# Automation Progress Monitor
# This script monitors the automated manuscript finalization

echo "=========================================="
echo "🤖 Automation Progress Monitor"
echo "=========================================="
echo ""

# Check if automation is running
if pgrep -f "AUTOMATED_MANUSCRIPT_FINALIZATION.py" > /dev/null; then
    echo "✅ Automation is RUNNING"
    echo ""
else
    echo "⚠️  Automation has COMPLETED or STOPPED"
    echo ""
fi

# Show recent progress
echo "📊 Recent Progress (last 30 lines):"
echo "=========================================="
tail -30 automation_execution.log 2>/dev/null || echo "Log file not yet available"
echo ""

# Check for completion
if [ -f "AUTOMATION_SUMMARY.json" ]; then
    echo "✅ Automation Summary Available!"
    echo "=========================================="
    cat AUTOMATION_SUMMARY.json
    echo ""
fi

# Check for generated files
echo "📁 Generated Files:"
echo "=========================================="
[ -f "SUPPLEMENTARY_MATERIALS.md" ] && echo "✓ SUPPLEMENTARY_MATERIALS.md" || echo "⏳ SUPPLEMENTARY_MATERIALS.md (pending)"
[ -f "MANUSCRIPT_bioRxiv_SUBMISSION.pdf" ] && echo "✓ MANUSCRIPT_bioRxiv_SUBMISSION.pdf" || echo "⏳ MANUSCRIPT_bioRxiv_SUBMISSION.pdf (pending)"
[ -d "outputs/enrichment_analysis" ] && echo "✓ outputs/enrichment_analysis/" || echo "⏳ outputs/enrichment_analysis/ (pending)"
[ -f "AUTOMATION_SUMMARY.json" ] && echo "✓ AUTOMATION_SUMMARY.json" || echo "⏳ AUTOMATION_SUMMARY.json (pending)"
echo ""

echo "=========================================="
echo "🔄 To monitor in real-time, run:"
echo "   tail -f automation_execution.log"
echo "=========================================="
