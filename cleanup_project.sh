#!/bin/bash
# 專案檔案結構整理腳本
# 執行時間：2025-11-02

echo "=========================================="
echo "  專案檔案結構整理開始"
echo "=========================================="

# Phase 1: 創建新目錄結構
echo -e "\n[Phase 1] 創建新目錄結構..."

mkdir -p docs/guides
mkdir -p docs/submission
mkdir -p docs/status
mkdir -p docs/excellence
mkdir -p docs/archive/execution_2025-11-02
mkdir -p docs/archive/assessments

mkdir -p paper/archive
mkdir -p paper/scripts_archive

mkdir -p scripts/excellence_upgrade
mkdir -p scripts/tcga_analysis
mkdir -p scripts/survival_analysis
mkdir -p scripts/figure_generation
mkdir -p scripts/llps_analysis
mkdir -p scripts/structure_prediction
mkdir -p scripts/data_download
mkdir -p scripts/quick_analysis
mkdir -p scripts/functional_analysis
mkdir -p scripts/literature_tools
mkdir -p scripts/nature_enhancement

mkdir -p outputs/figures_final
mkdir -p outputs/tables
mkdir -p outputs/figures_archive

echo "  ✓ 所有目錄已創建"

# Phase 2: 移動 docs/ 相關文件
echo -e "\n[Phase 2] 整理文檔目錄..."

# 移至 docs/guides/
mv -f QUICK_START_GUIDE.md docs/guides/ 2>/dev/null || true
mv -f PROMPTS.md docs/guides/ 2>/dev/null || true
mv -f FINAL_INSTRUCTIONS.md docs/guides/ 2>/dev/null || true

# 移至 docs/submission/
mv -f MANUSCRIPT_WITHDRAWAL_LETTER.md docs/submission/ 2>/dev/null || true
mv -f paper/BIORXIV_SUBMISSION_GUIDE.md docs/submission/ 2>/dev/null || true

# 移至 docs/archive/execution_2025-11-02/
mv -f EXECUTION_SUCCESS_REPORT.md docs/archive/execution_2025-11-02/ 2>/dev/null || true
mv -f READY_TO_EXECUTE.md docs/archive/execution_2025-11-02/ 2>/dev/null || true
mv -f EXCELLENCE_EXECUTION_GUIDE.md docs/archive/execution_2025-11-02/ 2>/dev/null || true
mv -f EXCELLENCE_UPGRADE_PLAN.md docs/archive/execution_2025-11-02/ 2>/dev/null || true

# 移至 docs/archive/assessments/
mv -f HONEST_TRUTH_REPORT.md docs/archive/assessments/ 2>/dev/null || true
mv -f NOVELTY_VALIDATION_FINAL.md docs/archive/assessments/ 2>/dev/null || true

# 移至 docs/excellence/
mv -f docs/excellence/EXCELLENCE_ASSESSMENT.md docs/excellence/ 2>/dev/null || true
mv -f docs/excellence/EXCELLENCE_PLAN.md docs/excellence/ 2>/dev/null || true
mv -f docs/excellence/FINAL_EXCELLENCE_SUMMARY.md docs/excellence/ 2>/dev/null || true

echo "  ✓ 文檔已整理"

# Phase 3: 整理 paper/ 目錄
echo -e "\n[Phase 3] 整理論文目錄..."

# 重命名當前版本
cd paper
cp -f biorxiv_clean.md manuscript_v2.md 2>/dev/null || true
cp -f biorxiv_OPTIMIZED.pdf manuscript_v2_optimized.pdf 2>/dev/null || true

# 移動舊版 PDF
mv -f biorxiv_FINAL.pdf archive/ 2>/dev/null || true
mv -f biorxiv_manuscript.pdf archive/ 2>/dev/null || true
mv -f biorxiv_PERFECT.pdf archive/ 2>/dev/null || true

# 移動舊版 MD
mv -f biorxiv_manuscript.md archive/ 2>/dev/null || true
mv -f preprint_outline.md archive/ 2>/dev/null || true
mv -f preprint_outline_v2_evidence_based.md archive/ 2>/dev/null || true

# 移動舊腳本
mv -f convert_clean_to_pdf.py scripts_archive/ 2>/dev/null || true
mv -f generate_pdf.py scripts_archive/ 2>/dev/null || true
mv -f generate_html_pdf.py scripts_archive/ 2>/dev/null || true
mv -f generate_professional_pdf.py scripts_archive/ 2>/dev/null || true
mv -f generate_perfect_pdf.py scripts_archive/ 2>/dev/null || true

# 移動批次檔
mv -f CONVERT_TO_PDF.bat scripts_archive/ 2>/dev/null || true
mv -f OPEN_AND_PRINT.bat scripts_archive/ 2>/dev/null || true

cd ..
echo "  ✓ 論文目錄已整理"

# Phase 4: 整理 scripts/ 目錄
echo -e "\n[Phase 4] 整理腳本目錄..."

# excellence_upgrade/
mv -f scripts/stage2_multivariate_cox.py scripts/excellence_upgrade/ 2>/dev/null || true
mv -f scripts/stage3_partial_correlation.py scripts/excellence_upgrade/ 2>/dev/null || true
mv -f scripts/stage4_cptac_validation.py scripts/excellence_upgrade/ 2>/dev/null || true

# nature_enhancement/
mv -f scripts/automated_nature_enhancement.py scripts/nature_enhancement/ 2>/dev/null || true
mv -f scripts/nature_level_enhancement.py scripts/nature_enhancement/ 2>/dev/null || true
mv -f scripts/generate_nature_figures.py scripts/nature_enhancement/ 2>/dev/null || true
mv -f scripts/deep_computational_contributions.py scripts/nature_enhancement/ 2>/dev/null || true

# tcga_analysis/
mv -f scripts/tcga_full_cohort_analysis.py scripts/tcga_analysis/ 2>/dev/null || true
mv -f scripts/tcga_join_and_analyze.py scripts/tcga_analysis/ 2>/dev/null || true
mv -f scripts/tcga_survival.py scripts/tcga_analysis/ 2>/dev/null || true
mv -f scripts/tcga_survival_analysis.py scripts/tcga_analysis/ 2>/dev/null || true
mv -f scripts/gdc_expression_2025.py scripts/tcga_analysis/ 2>/dev/null || true
mv -f scripts/download_mega_tcga_cohort.py scripts/tcga_analysis/ 2>/dev/null || true
mv -f scripts/xena_tcga_expression.py scripts/tcga_analysis/ 2>/dev/null || true
mv -f scripts/plot_tcga.py scripts/tcga_analysis/ 2>/dev/null || true

# survival_analysis/
mv -f scripts/enhanced_survival_analysis.py scripts/survival_analysis/ 2>/dev/null || true
mv -f scripts/real_survival_analysis.py scripts/survival_analysis/ 2>/dev/null || true
mv -f scripts/gdc_clinical_survival.py scripts/survival_analysis/ 2>/dev/null || true

# figure_generation/
mv -f scripts/auto_generate_figures.py scripts/figure_generation/ 2>/dev/null || true
mv -f scripts/regenerate_figure2.py scripts/figure_generation/ 2>/dev/null || true
mv -f scripts/regenerate_figure3.py scripts/figure_generation/ 2>/dev/null || true

# llps_analysis/
mv -f scripts/genome_scale_llps_scan.py scripts/llps_analysis/ 2>/dev/null || true
mv -f scripts/saprot_llps_prediction.py scripts/llps_analysis/ 2>/dev/null || true
mv -f scripts/saprot_real_inference.py scripts/llps_analysis/ 2>/dev/null || true
mv -f scripts/integrated_llps_platform.py scripts/llps_analysis/ 2>/dev/null || true
mv -f scripts/auto_generate_llps_guidelines.py scripts/llps_analysis/ 2>/dev/null || true

# structure_prediction/
mv -f scripts/download_alphafold_structures.py scripts/structure_prediction/ 2>/dev/null || true
mv -f scripts/prepare_alphafold_sequences.py scripts/structure_prediction/ 2>/dev/null || true
mv -f scripts/foldseek_encode_structures.py scripts/structure_prediction/ 2>/dev/null || true

# data_download/
mv -f scripts/cbioportal_fetch.py scripts/data_download/ 2>/dev/null || true
mv -f scripts/cbioportal_genomics.py scripts/data_download/ 2>/dev/null || true
mv -f scripts/depmap_download.py scripts/data_download/ 2>/dev/null || true
mv -f scripts/gdc_query.py scripts/data_download/ 2>/dev/null || true

# quick_analysis/
mv -f scripts/quick_correlation_analysis.py scripts/quick_analysis/ 2>/dev/null || true
mv -f scripts/quick_partial_analysis.py scripts/quick_analysis/ 2>/dev/null || true

# functional_analysis/
mv -f scripts/pathway_enrichment_analysis.py scripts/functional_analysis/ 2>/dev/null || true

# literature_tools/
mv -f scripts/pubmed_triage.py scripts/literature_tools/ 2>/dev/null || true
mv -f scripts/auto_literature_gap_analysis.py scripts/literature_tools/ 2>/dev/null || true
mv -f scripts/auto_update_preprint_outline.py scripts/literature_tools/ 2>/dev/null || true
mv -f scripts/validate_novelty.py scripts/literature_tools/ 2>/dev/null || true

echo "  ✓ 腳本目錄已整理"

# Phase 5: 整理 outputs/ 目錄
echo -e "\n[Phase 5] 整理輸出目錄..."

# 複製最終圖至 figures_final/ 並重命名
cp -f outputs/figures/Figure2_TCGA_Correlation.png outputs/figures_final/Figure1_Correlation_Heatmap.png 2>/dev/null || true
cp -f outputs/tcga_full_cohort/TCGA_Full_Cohort_Analysis.png outputs/figures_final/Figure2_TCGA_4Panel_Analysis.png 2>/dev/null || true
cp -f outputs/survival_analysis_v2/Figure3_multivariate_cox.png outputs/figures_final/Figure3_Multivariate_Cox_Survival.png 2>/dev/null || true
cp -f outputs/partial_correlation/Figure_S2_partial_correlation.png outputs/figures_final/FigureS2_Partial_Correlation_6Panel.png 2>/dev/null || true
cp -f outputs/cptac_validation/Figure4_cptac_validation.png outputs/figures_final/Figure4_CPTAC_Protein_Validation.png 2>/dev/null || true

# 移動舊圖至 archive
mv -f outputs/survival_analysis outputs/figures_archive/ 2>/dev/null || true
mv -f outputs/gdc_expression outputs/figures_archive/ 2>/dev/null || true
mv -f outputs/figures/Figure1_Literature_Gap.png outputs/figures_archive/ 2>/dev/null || true
mv -f outputs/figures/Figure3_Methodological_Framework.png outputs/figures_archive/ 2>/dev/null || true

# 複製結果表至 tables/
cp -f outputs/survival_analysis_v2/multivariate_cox_results.csv outputs/tables/Table2_cox_results.csv 2>/dev/null || true
cp -f outputs/partial_correlation/Table3_partial_correlation.csv outputs/tables/Table3_partial_correlation.csv 2>/dev/null || true
cp -f outputs/tcga_full_cohort/correlation_results.csv outputs/tables/Table1_correlations.csv 2>/dev/null || true

echo "  ✓ 輸出目錄已整理"

# Phase 6: 刪除過時文件
echo -e "\n[Phase 6] 刪除過時文件..."

rm -f FINAL_SUMMARY.md 2>/dev/null || true
rm -f SUCCESS_SUMMARY.md 2>/dev/null || true
rm -f WAKE_UP_SUMMARY.md 2>/dev/null || true
rm -f OVERNIGHT_EXECUTION_PLAN.md 2>/dev/null || true
rm -f RELEASE_NOTES_v1.0.0.md 2>/dev/null || true
rm -f START_NOW.bat 2>/dev/null || true
rm -f RUN_OVERNIGHT_ENHANCEMENT.bat 2>/dev/null || true
rm -f run_excellence_upgrade.bat 2>/dev/null || true
rm -f run_excellence_upgrade.sh 2>/dev/null || true

echo "  ✓ 過時文件已刪除"

# Phase 7: 創建 README 文件
echo -e "\n[Phase 7] 創建目錄 README..."

# scripts/excellence_upgrade/README.md
cat > scripts/excellence_upgrade/README.md << 'EOF'
# Excellence Upgrade Scripts

**執行日期**: 2025-11-02

這些腳本用於將論文提升至 Nature Communications 水準。

## 腳本說明

- `stage2_multivariate_cox.py` - 多變項 Cox 生存分析
- `stage3_partial_correlation.py` - 偏相關分析（控制混雜因子）
- `stage4_cptac_validation.py` - CPTAC 蛋白質層驗證

## 執行結果

所有三個階段已成功執行並生成輸出。詳見 `docs/archive/execution_2025-11-02/EXECUTION_SUCCESS_REPORT.md`
EOF

echo "  ✓ README 文件已創建"

echo -e "\n=========================================="
echo "  ✓ 專案整理完成！"
echo "=========================================="
echo ""
echo "新結構摘要："
echo "  - docs/       : 所有文檔已分類"
echo "  - paper/      : 當前版本 + archive"
echo "  - scripts/    : 腳本已分類至 11 個子目錄"
echo "  - outputs/    : figures_final + tables + archive"
echo ""
echo "下一步："
echo "  1. 檢查 paper/manuscript_v2_optimized.pdf"
echo "  2. 查看 docs/submission/ 中的投稿指南"
echo "  3. 使用 outputs/figures_final/ 中的最終圖"
echo ""
