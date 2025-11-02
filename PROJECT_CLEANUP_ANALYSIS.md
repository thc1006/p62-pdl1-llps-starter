# 🧹 專案檔案結構清理分析

**分析時間**: 2025-11-02
**目標**: 整潔、清晰、一目了然的專案結構

---

## 📊 當前狀態分析

### **根目錄混亂問題** ⚠️

目前根目錄有 **30+ 個 Markdown 文件**，造成混亂：

#### **卓越升級系列（已完成）** ✅ → 移至 `docs/archive/`
```
EXCELLENCE_EXECUTION_GUIDE.md      ← 已執行完成
EXCELLENCE_UPGRADE_PLAN.md         ← 已執行完成
EXECUTION_SUCCESS_REPORT.md        ← 執行報告
READY_TO_EXECUTE.md                ← 執行指南
```
**決策**: 移至 `docs/archive/execution_2025-11-02/`（歷史記錄）

#### **評估報告系列（歷史文件）** 📚 → 移至 `docs/archive/`
```
HONEST_TRUTH_REPORT.md             ← 誠實評估報告
NOVELTY_VALIDATION_FINAL.md       ← 新穎性驗證
FINAL_EXCELLENCE_SUMMARY.md       ← 卓越總結
```
**決策**: 移至 `docs/archive/assessments/`

#### **撤稿信範本（當前有用）** ✅ → 保留在 `docs/submission/`
```
MANUSCRIPT_WITHDRAWAL_LETTER.md   ← 當前有用
```
**決策**: 移至 `docs/submission/`

#### **過時的摘要文件** ❌ → 刪除或合併
```
FINAL_SUMMARY.md                   ← 過時
SUCCESS_SUMMARY.md                 ← 過時
WAKE_UP_SUMMARY.md                 ← 過時
OVERNIGHT_EXECUTION_PLAN.md       ← 已執行完成
```
**決策**: 刪除（內容已整合至 EXECUTION_SUCCESS_REPORT.md）

#### **專案狀態文件（需更新）** 🔄 → 更新並移至 `docs/`
```
PROJECT_STATUS.md                  ← 需更新
REVISION_SUMMARY.md                ← 需更新
RELEASE_NOTES_v1.0.0.md           ← 已過時
```
**決策**: 更新 PROJECT_STATUS.md 移至 `docs/`，刪除其他

#### **指南文件（保留）** ✅ → 移至 `docs/guides/`
```
QUICK_START_GUIDE.md               ← 保留
PROMPTS.md                         ← 保留
FINAL_INSTRUCTIONS.md              ← 保留
```
**決策**: 移至 `docs/guides/`

---

### **paper/ 目錄問題** 📄

#### **多個 PDF 版本** ⚠️
```
biorxiv_FINAL.pdf          (1.4M) ← 舊版
biorxiv_manuscript.pdf     (1.3M) ← 舊版
biorxiv_PERFECT.pdf        (1.9M) ← 舊版（未優化）
biorxiv_OPTIMIZED.pdf      (2.1M) ← ✅ 最新版（使用此版本）
```
**決策**:
- 保留 `biorxiv_OPTIMIZED.pdf` → 重命名為 `manuscript_v2_optimized.pdf`
- 其他移至 `paper/archive/`

#### **多個 Python 腳本** 🐍
```
convert_clean_to_pdf.py            ← 舊版
generate_pdf.py                    ← 舊版
generate_html_pdf.py               ← 舊版
generate_professional_pdf.py       ← 舊版
generate_perfect_pdf.py            ← 舊版
generate_optimized_pdf.py          ← ✅ 最新版
```
**決策**: 保留 `generate_optimized_pdf.py`，其他移至 `paper/scripts_archive/`

#### **Markdown 文件** 📝
```
biorxiv_clean.md                   ← ✅ 當前版本
biorxiv_manuscript.md              ← 舊版
preprint_outline.md                ← 舊版
preprint_outline_v2_evidence_based.md ← 舊版
```
**決策**: 保留 `biorxiv_clean.md`，重命名為 `manuscript_v2.md`，其他移至 `paper/archive/`

---

### **scripts/ 目錄問題** 🔧

#### **已執行完成的腳本** ✅ → 移至專用目錄
```
stage2_multivariate_cox.py         ← 已執行（Stage 2）
stage3_partial_correlation.py      ← 已執行（Stage 3）
stage4_cptac_validation.py         ← 已執行（Stage 4）
```
**決策**: 移至 `scripts/excellence_upgrade/`（保留以供重現）

#### **Nature 級別增強腳本** 🌟 → 歸類
```
automated_nature_enhancement.py    ← Nature 增強
nature_level_enhancement.py        ← Nature 增強
generate_nature_figures.py         ← Nature 圖生成
deep_computational_contributions.py ← 深度計算
```
**決策**: 移至 `scripts/nature_enhancement/`

#### **TCGA 數據分析腳本** 📊 → 歸類
```
tcga_full_cohort_analysis.py       ← TCGA 完整分析
tcga_join_and_analyze.py           ← TCGA 合併分析
tcga_survival.py                   ← 生存分析
tcga_survival_analysis.py          ← 生存分析
gdc_expression_2025.py             ← GDC 表達數據
download_mega_tcga_cohort.py       ← TCGA 下載
xena_tcga_expression.py            ← Xena 表達數據
```
**決策**: 移至 `scripts/tcga_analysis/`

#### **生存分析腳本** 📈 → 歸類
```
enhanced_survival_analysis.py      ← 增強生存分析
real_survival_analysis.py          ← 真實生存分析
gdc_clinical_survival.py           ← 臨床生存數據
```
**決策**: 移至 `scripts/survival_analysis/`

#### **快速分析腳本** ⚡ → 歸類
```
quick_correlation_analysis.py      ← 快速相關分析
quick_partial_analysis.py          ← 快速偏相關
```
**決策**: 移至 `scripts/quick_analysis/`

#### **圖生成腳本** 📊 → 歸類
```
auto_generate_figures.py           ← 自動圖生成
regenerate_figure2.py              ← 重生成 Figure 2
regenerate_figure3.py              ← 重生成 Figure 3
plot_tcga.py                       ← TCGA 繪圖
```
**決策**: 移至 `scripts/figure_generation/`

#### **LLPS 相關腳本** 🧬 → 歸類
```
genome_scale_llps_scan.py          ← 基因組級 LLPS
saprot_llps_prediction.py          ← SaProt LLPS 預測
saprot_real_inference.py           ← SaProt 推理
integrated_llps_platform.py        ← 整合 LLPS 平台
auto_generate_llps_guidelines.py   ← LLPS 指南
```
**決策**: 移至 `scripts/llps_analysis/`

#### **AlphaFold 相關腳本** 🔬 → 歸類
```
download_alphafold_structures.py   ← AlphaFold 下載
prepare_alphafold_sequences.py     ← 序列準備
foldseek_encode_structures.py      ← FoldSeek 編碼
```
**決策**: 移至 `scripts/structure_prediction/`

#### **其他腳本** 🔧 → 歸類
```
cbioportal_fetch.py                ← cBioPortal 獲取
cbioportal_genomics.py             ← cBioPortal 基因組
depmap_download.py                 ← DepMap 下載
pathway_enrichment_analysis.py     ← 通路富集
pubmed_triage.py                   ← PubMed 篩選
auto_literature_gap_analysis.py    ← 文獻差距分析
auto_update_preprint_outline.py    ← 預印本更新
validate_novelty.py                ← 新穎性驗證
```
**決策**:
- cBioPortal → `scripts/data_download/`
- DepMap → `scripts/data_download/`
- 通路富集 → `scripts/functional_analysis/`
- 文獻相關 → `scripts/literature_tools/`

---

### **outputs/ 目錄問題** 📂

#### **圖片文件** 🖼️
```
outputs/figures/                   ← 3 張圖（主要圖）
outputs/tcga_full_cohort/          ← 2 張圖（TCGA 分析）
outputs/survival_analysis/         ← 2 張圖（舊生存分析）
outputs/survival_analysis_v2/      ← 1 張圖（新多變項 Cox）
outputs/partial_correlation/       ← 1 張圖（偏相關）
outputs/cptac_validation/          ← 1 張圖（CPTAC 驗證）
outputs/gdc_expression/            ← 1 張圖（舊相關圖）
```
**決策**:
- 創建 `outputs/figures_final/` 存放論文用圖
- 舊圖移至 `outputs/figures_archive/`

#### **最終論文圖（5 張）** ✅
```
Figure1: figures/Figure2_TCGA_Correlation.png (349K)
Figure2: tcga_full_cohort/TCGA_Full_Cohort_Analysis.png (439K)
Figure3: survival_analysis_v2/Figure3_multivariate_cox.png (621K)
FigureS2: partial_correlation/Figure_S2_partial_correlation.png (1.1M)
Figure4: cptac_validation/Figure4_cptac_validation.png (729K)
```
**決策**: 複製至 `outputs/figures_final/` 並重命名

---

## 🎯 整理計劃

### **新的專案結構**

```
p62-pdl1-llps-starter/
├── README.md                          ✅ 保留（主要入口）
├── CLAUDE.md                          ✅ 保留（專案說明）
├── LICENSE                            ✅ 保留
├── .gitignore                         ✅ 保留
│
├── docs/                              📚 文檔目錄
│   ├── guides/                        ✅ 使用指南
│   │   ├── QUICK_START_GUIDE.md
│   │   ├── PROMPTS.md
│   │   ├── FINAL_INSTRUCTIONS.md
│   │   └── 專案總結報告_繁體中文.md
│   │
│   ├── submission/                    📤 投稿相關
│   │   ├── MANUSCRIPT_WITHDRAWAL_LETTER.md
│   │   └── BIORXIV_SUBMISSION_GUIDE.md
│   │
│   ├── status/                        📊 專案狀態
│   │   └── PROJECT_STATUS_v2.md       ← 更新版
│   │
│   ├── excellence/                    🌟 卓越評估（歷史）
│   │   ├── EXCELLENCE_ASSESSMENT.md
│   │   ├── EXCELLENCE_PLAN.md
│   │   └── FINAL_EXCELLENCE_SUMMARY.md
│   │
│   └── archive/                       📦 歷史文檔
│       ├── execution_2025-11-02/      ← 執行記錄
│       │   ├── EXECUTION_SUCCESS_REPORT.md
│       │   ├── READY_TO_EXECUTE.md
│       │   ├── EXCELLENCE_EXECUTION_GUIDE.md
│       │   └── EXCELLENCE_UPGRADE_PLAN.md
│       │
│       └── assessments/               ← 評估報告
│           ├── HONEST_TRUTH_REPORT.md
│           └── NOVELTY_VALIDATION_FINAL.md
│
├── paper/                             📄 論文目錄
│   ├── manuscript_v2.md               ✅ 當前版本
│   ├── manuscript_v2_optimized.pdf    ✅ 最終 PDF
│   ├── generate_optimized_pdf.py      ✅ PDF 生成腳本
│   │
│   ├── archive/                       📦 舊版本
│   │   ├── biorxiv_manuscript.md
│   │   ├── preprint_outline.md
│   │   ├── biorxiv_FINAL.pdf
│   │   ├── biorxiv_PERFECT.pdf
│   │   └── ...
│   │
│   └── scripts_archive/               🔧 舊腳本
│       ├── convert_clean_to_pdf.py
│       ├── generate_pdf.py
│       └── ...
│
├── scripts/                           🔧 腳本目錄
│   ├── excellence_upgrade/            ✅ 卓越升級（已執行）
│   │   ├── stage2_multivariate_cox.py
│   │   ├── stage3_partial_correlation.py
│   │   └── stage4_cptac_validation.py
│   │
│   ├── tcga_analysis/                 📊 TCGA 分析
│   │   ├── tcga_full_cohort_analysis.py
│   │   ├── tcga_join_and_analyze.py
│   │   └── ...
│   │
│   ├── survival_analysis/             📈 生存分析
│   │   ├── enhanced_survival_analysis.py
│   │   ├── real_survival_analysis.py
│   │   └── gdc_clinical_survival.py
│   │
│   ├── figure_generation/             📊 圖生成
│   │   ├── auto_generate_figures.py
│   │   ├── regenerate_figure2.py
│   │   └── ...
│   │
│   ├── llps_analysis/                 🧬 LLPS 分析
│   │   ├── genome_scale_llps_scan.py
│   │   ├── saprot_llps_prediction.py
│   │   └── ...
│   │
│   ├── structure_prediction/          🔬 結構預測
│   │   ├── download_alphafold_structures.py
│   │   └── ...
│   │
│   ├── data_download/                 📥 數據下載
│   │   ├── cbioportal_fetch.py
│   │   ├── depmap_download.py
│   │   └── ...
│   │
│   ├── quick_analysis/                ⚡ 快速分析
│   │   ├── quick_correlation_analysis.py
│   │   └── quick_partial_analysis.py
│   │
│   ├── functional_analysis/           🧪 功能分析
│   │   └── pathway_enrichment_analysis.py
│   │
│   └── literature_tools/              📚 文獻工具
│       ├── pubmed_triage.py
│       ├── auto_literature_gap_analysis.py
│       └── validate_novelty.py
│
├── outputs/                           📂 輸出目錄
│   ├── figures_final/                 ✅ 最終論文圖
│   │   ├── Figure1_Correlation_Heatmap.png
│   │   ├── Figure2_TCGA_4Panel_Analysis.png
│   │   ├── Figure3_Multivariate_Cox_Survival.png
│   │   ├── FigureS2_Partial_Correlation_6Panel.png
│   │   └── Figure4_CPTAC_Protein_Validation.png
│   │
│   ├── tables/                        📊 結果表格
│   │   ├── Table1_correlations.csv
│   │   ├── Table2_cox_results.csv
│   │   ├── Table3_partial_correlation.csv
│   │   └── ...
│   │
│   ├── survival_analysis_v2/          📈 新生存分析
│   ├── partial_correlation/           🔬 偏相關分析
│   ├── cptac_validation/              🧬 CPTAC 驗證
│   │
│   └── figures_archive/               📦 舊圖存檔
│       ├── survival_analysis/
│       ├── gdc_expression/
│       └── ...
│
├── data/                              💾 數據目錄
├── tools/                             🛠️ 工具目錄
├── workflows/                         🔄 工作流程
├── skills/                            🎯 技能模組
├── protocols/                         📋 實驗方案
└── .claude/                           ⚙️ Claude 配置

```

---

## 🚀 執行計劃

### **Phase 1: 創建新結構** ✅
1. 創建所有新目錄
2. 移動 `docs/` 相關文件
3. 整理 `paper/` 目錄

### **Phase 2: 整理 scripts/** 🔧
1. 創建分類子目錄
2. 移動腳本至對應目錄
3. 創建各目錄的 README.md

### **Phase 3: 整理 outputs/** 📊
1. 創建 `figures_final/`
2. 複製最終圖並重命名
3. 移動舊圖至 `figures_archive/`

### **Phase 4: 清理根目錄** 🧹
1. 刪除過時文件
2. 移動歷史文件至 archive
3. 更新 README.md

---

## 📋 檔案處理清單

### **刪除的文件** ❌
```
FINAL_SUMMARY.md                   ← 內容已整合
SUCCESS_SUMMARY.md                 ← 內容已整合
WAKE_UP_SUMMARY.md                 ← 內容已整合
OVERNIGHT_EXECUTION_PLAN.md       ← 已執行完成
RELEASE_NOTES_v1.0.0.md           ← 已過時
START_NOW.bat                      ← 不需要
RUN_OVERNIGHT_ENHANCEMENT.bat     ← 已執行完成
```

### **移至 archive/ 的文件** 📦
```
execution_2025-11-02/:
  - EXECUTION_SUCCESS_REPORT.md
  - READY_TO_EXECUTE.md
  - EXCELLENCE_EXECUTION_GUIDE.md
  - EXCELLENCE_UPGRADE_PLAN.md

assessments/:
  - HONEST_TRUTH_REPORT.md
  - NOVELTY_VALIDATION_FINAL.md
```

### **重命名的文件** 🔄
```
biorxiv_clean.md                   → manuscript_v2.md
biorxiv_OPTIMIZED.pdf              → manuscript_v2_optimized.pdf
```

---

**準備執行整理！**
