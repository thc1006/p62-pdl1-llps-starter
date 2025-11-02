#!/bin/bash
# 全自動執行腳本
set -e

echo "================================"
echo "全自動管線執行開始"
echo "時間: $(date)"
echo "================================"

# 啟動虛擬環境
source venv/bin/activate

# Phase 2C - 使用修復後的腳本
echo ""
echo "[Phase 2C] 執行 Partial Correlation (TIMER2.0 + Parallel)"
python scripts/excellence_upgrade/stage3_v3_timer2_confounders_parallel.py 2>&1 | tee logs/phase_2c_final.log
if [ $? -eq 0 ]; then
    echo "[Phase 2C] ✅ 成功"
    # 複製到 Phase 3A/3B 期望的位置
    mkdir -p outputs/partial_correlation_v3_timer2
    cp outputs/partial_correlation_v3_timer2_parallel/partial_correlation_results_timer2_parallel.csv \
       outputs/partial_correlation_v3_timer2/partial_correlation_results_timer2.csv
else
    echo "[Phase 2C] ❌ 失敗"
    exit 1
fi

# Phase 3A - Single-cell validation
echo ""
echo "[Phase 3A] 執行 Single-cell Validation"
python scripts/analysis/single_cell_validation.py 2>&1 | tee logs/phase_3a_final.log
if [ $? -eq 0 ]; then
    echo "[Phase 3A] ✅ 成功"
else
    echo "[Phase 3A] ❌ 失敗"
fi

# Phase 3B - External validation
echo ""
echo "[Phase 3B] 執行 External Validation (GEO)"
python scripts/analysis/external_validation_geo.py 2>&1 | tee logs/phase_3b_final.log
if [ $? -eq 0 ]; then
    echo "[Phase 3B] ✅ 成功"
else
    echo "[Phase 3B] ❌ 失敗"
fi

echo ""
echo "================================"
echo "管線執行完成"
echo "時間: $(date)"
echo "================================"
echo ""
echo "查看結果:"
echo "  - Phase 2C: outputs/partial_correlation_v3_timer2_parallel/"
echo "  - Phase 3A: outputs/single_cell_validation/"
echo "  - Phase 3B: outputs/external_validation/"
