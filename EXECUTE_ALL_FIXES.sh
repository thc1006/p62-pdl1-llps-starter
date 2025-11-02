#!/bin/bash
# 自動化執行所有修復 - 榨乾電腦效能版本
# 支援 Docker, WSL, GPU 加速

set -e  # Exit on error

echo "========================================================================"
echo "🚀 EXCELLENCE UPGRADE - AUTOMATED EXECUTION"
echo "========================================================================"
echo ""
echo "This script will:"
echo "  ✓ Fix circular adjustment in IFN-γ/immune scores"
echo "  ✓ Fix cross-cancer Cox analysis"
echo "  ✓ Add Schoenfeld residuals test"
echo "  ✓ Add Spearman correlation + bootstrap CI"
echo "  ✓ Add VIF multicollinearity check"
echo ""
echo "Environment detected:"
echo "  - OS: $(uname -s)"
echo "  - Python: $(python3 --version 2>/dev/null || echo 'Not found')"
echo "  - Docker: $(docker --version 2>/dev/null || echo 'Not installed')"
echo "  - GPU: $(nvidia-smi --query-gpu=name --format=csv,noheader 2>/dev/null || echo 'No NVIDIA GPU')"
echo ""
echo "========================================================================"

# ============================================================================
# Choose execution method
# ============================================================================
echo ""
echo "Choose execution method:"
echo "  1) Native Python (fastest, requires dependencies installed)"
echo "  2) Docker (isolated, no dependency issues)"
echo "  3) Docker + GPU (if you have NVIDIA GPU)"
echo ""
read -p "Enter choice [1-3]: " choice

case $choice in
    1)
        echo ""
        echo "▶️ Executing with native Python..."
        python3 scripts/excellence_upgrade/AUTOMATE_ALL_FIXES.py
        ;;

    2)
        echo ""
        echo "▶️ Building Docker image..."
        docker build -t pdl1-excellence -f docker/Dockerfile.excellence .

        echo ""
        echo "▶️ Running in Docker container..."
        docker run --rm \
            -v "$(pwd)":/workspace \
            -v "$(pwd)/outputs":/workspace/outputs \
            -v "$(pwd)/data":/workspace/data \
            pdl1-excellence
        ;;

    3)
        echo ""
        echo "▶️ Checking GPU availability..."
        if ! nvidia-smi &> /dev/null; then
            echo "❌ ERROR: nvidia-smi not found. Do you have NVIDIA GPU drivers installed?"
            exit 1
        fi

        echo "✅ GPU detected:"
        nvidia-smi --query-gpu=name,memory.total --format=csv,noheader

        echo ""
        echo "▶️ Building Docker image with CUDA support..."
        docker build -t pdl1-excellence-gpu -f docker/Dockerfile.excellence .

        echo ""
        echo "▶️ Running in Docker container with GPU..."
        docker run --rm \
            --gpus all \
            -v "$(pwd)":/workspace \
            -v "$(pwd)/outputs":/workspace/outputs \
            -v "$(pwd)/data":/workspace/data \
            pdl1-excellence-gpu
        ;;

    *)
        echo "❌ Invalid choice"
        exit 1
        ;;
esac

# ============================================================================
# Post-execution summary
# ============================================================================
echo ""
echo "========================================================================"
echo "✅ EXECUTION COMPLETED"
echo "========================================================================"
echo ""
echo "📂 Check outputs in:"
echo "  - outputs/survival_analysis_v2_fixed/"
echo "  - outputs/partial_correlation_v2_fixed/"
echo "  - outputs/excellence_upgrade_results/"
echo ""
echo "📄 Next steps:"
echo "  1. Review execution results JSON"
echo "  2. Inspect generated figures and tables"
echo "  3. Update manuscript with corrected methodology"
echo "  4. Commit and push changes to GitHub"
echo ""
echo "🎯 Target journals:"
echo "  - Genome Medicine (IF ~10)"
echo "  - J ImmunoTher Cancer (IF ~10)"
echo "  - Nature Communications (IF ~16) - with additional validation"
echo ""
echo "========================================================================"
