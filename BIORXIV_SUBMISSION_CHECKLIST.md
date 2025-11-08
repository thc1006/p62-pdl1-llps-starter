# bioRxiv 投稿檢查清單

**最後更新**: 2025-11-08
**手稿檔案**: `MANUSCRIPT_bioRxiv_SUBMISSION_FINAL.pdf`
**專案狀態**: ✅ **準備就緒，可立即投稿**

---

## 📋 快速總覽

| 項目 | 狀態 | 備註 |
|------|------|------|
| 最終 PDF 檔案 | ✅ | 2.7 MB, 32 頁 |
| 手稿完整性 | ✅ | 所有章節完整 |
| 圖表嵌入 | ✅ | 6 張圖表已嵌入 |
| 表格嵌入 | ✅ | 5 張表格已嵌入 |
| 參考文獻 | ✅ | 完整引用格式 |
| 資料透明度聲明 | ✅ | 11 處明確標註模擬數據 |
| GitHub 倉庫 | ⚠️ | 需確認為公開狀態 |

---

## 🎯 手稿基本資訊

### 標題
```
Multi-Dimensional Integrative Analysis of PD-L1 Regulatory Networks:
A Computational Framework Integrating Large-Scale Genomics and Immune
Deconvolution Across 1,635 Cancer Patients
```

**短標題**（建議，如果期刊要求）：
```
Multi-Dimensional Analysis of PD-L1 Regulatory Networks
```

### 作者資訊
- **作者**: Hsiu-Chi Tsai
- **機構**: National Yang Ming Chiao Tung University, Hsinchu, Taiwan
- **通訊作者 Email**: hctsai1006@cs.nctu.edu.tw
- **ORCID**: （如有請填寫）

### 文章類型
- **推薦**: ✅ **New Results** (包含新發現的計算分析)
- 備選: Confirmatory Results (如果強調驗證性質)

### 學科領域
- **主要領域**: ✅ **Bioinformatics**
- **次要領域**: Cancer Biology, Systems Biology

---

## 📄 手稿內容核查

### ✅ 必要章節（全部完整）

- [x] **Title** - 清楚描述研究範圍和規模
- [x] **Authors & Affiliations** - 完整作者資訊
- [x] **Abstract** (結構化)
  - Background: PD-L1 調控網路的研究缺口
  - Methods: 四維整合分析框架（1,635 樣本）
  - Results: 主要發現（CMTM6-PD-L1, STUB1-PD-L1 相關性）
  - Conclusions: 建立計算框架範本
- [x] **Keywords** - 9 個關鍵詞
- [x] **Introduction** - 研究背景和動機
- [x] **Methods** - 完整方法學描述
  - 數據獲取和處理
  - TIMER2.0 免疫去卷積
  - 統計分析（相關性、偏相關、Cox 回歸）
  - 敏感度分析
- [x] **Results** - 主要發現
- [x] **Discussion** - 結果解釋和意義
- [x] **Conclusions** - 研究總結
- [x] **References** - 完整參考文獻
- [x] **Figure Legends** - 所有圖表說明
- [x] **Tables** - 數據表格

### ✅ 關鍵數據聲明

- [x] **樣本規模明確**: 1,635 TCGA 樣本
  - LUAD: n=601
  - LUSC: n=562
  - SKCM: n=472

- [x] **主要統計結果清楚**:
  - CMTM6-PD-L1: ρ=0.42, P=2.3×10⁻⁶⁸
  - Partial correlation: ρ=0.31 (74% retained)
  - STUB1-PD-L1: ρ=-0.15, P=6.2×10⁻¹⁰

- [x] **模擬數據明確標註**:
  - Abstract 中聲明
  - Methods 中詳細說明
  - Results 中每次提及都標註
  - 共 11 處明確聲明

### ✅ 科學透明度

- [x] **數據來源明確**: TCGA GDC Portal
- [x] **方法可重現**: 完整計算參數
- [x] **限制明確說明**:
  - 生存數據為模擬（proof-of-concept）
  - 缺乏實驗驗證
  - 相關性非因果關係
- [x] **代碼可獲得**: GitHub repository 連結
- [x] **無數據造假**: 所有表達數據來自真實 TCGA

---

## 🔬 技術規格核查

### PDF 檔案品質

- [x] **檔案大小**: 2.7 MB（<100 MB 限制）
- [x] **頁數**: 32 頁
- [x] **字體嵌入**: Times New Roman (mathptmx)
- [x] **圖表解析度**: 所有圖表高清晰度
- [x] **方程式渲染**: 數學符號正確顯示
- [x] **連結可點擊**: DOI 和 URL 可點擊

### 圖表檢查

**已嵌入 PDF 的圖表**:
- [x] Figure 1: Analytical Pipeline Overview
- [x] Figure 2: TCGA Expression Analysis
- [x] Figure 3: Correlation Analysis Results
- [x] Figure 4: Immune Deconvolution Results
- [x] Figure 5: Survival Analysis Framework (模擬數據)
- [x] Figure 6: Sensitivity Analysis Results

**所有圖表**:
- [x] 圖號與文中引用一致
- [x] 圖例完整清楚
- [x] 座標軸標示清楚
- [x] 統計顯著性標註（P 值、星號）

### 表格檢查

- [x] Table 1: Sample Characteristics
- [x] Table 2: Correlation Analysis Results
- [x] Table 3: Partial Correlation Results
- [x] Table 4: Cox Regression Results (模擬數據)
- [x] Table 5: Sensitivity Analysis Summary

---

## 📝 投稿表單資訊

### 基本資訊

**Manuscript Title**:
```
Multi-Dimensional Integrative Analysis of PD-L1 Regulatory Networks: A Computational Framework Integrating Large-Scale Genomics and Immune Deconvolution Across 1,635 Cancer Patients
```

**Article Type**: New Results

**Subject Areas**:
- Primary: Bioinformatics
- Secondary: Cancer Biology

**Keywords** (直接複製):
```
PD-L1, liquid-liquid phase separation, STUB1, CMTM6, cancer immunotherapy, TCGA, immune checkpoint, bioinformatics, computational biology
```

### Abstract（完整複製）

```
Background: PD-L1 (CD274) expression is a critical determinant of cancer immunotherapy response, yet the molecular regulatory networks governing its expression and stability across diverse tumor microenvironments remain incompletely characterized. While individual regulators have been identified, no comprehensive multi-dimensional framework exists to integrate transcriptomic, immune infiltration, and clinical outcome data at scale.

Methods: We developed and implemented a novel computational framework integrating four analytical dimensions to systematically dissect PD-L1 regulatory networks in 1,635 patients from The Cancer Genome Atlas (TCGA): (1) Large-scale genomic profiling of PD-L1 and LLPS-associated regulatory proteins (CMTM6, STUB1, HIP1R, SQSTM1) across three cancer types (LUAD, LUSC, SKCM); (2) Advanced immune deconvolution using TIMER2.0 to quantify six immune cell populations and their infiltration patterns; (3) Confounder-adjusted statistical modeling through partial correlation analysis controlling for immune microenvironment effects; (4) Proof-of-concept survival analysis framework using multivariate Cox proportional hazards regression with simulated survival outcomes (888 events) to demonstrate the analytical methodology, adjusting for age, sex, stage, and cancer type. We validated all transcriptomic findings through four sensitivity analysis approaches: cancer type-specific stratification (n=472-601 per stratum), outlier exclusion (Z-score, IQR, and MAD methods), bootstrap stability testing (1,000 iterations), and alternative statistical methods (Pearson, Spearman, Kendall correlations).

Results: Our integrative framework revealed complex PD-L1 regulatory patterns with robust statistical support: (1) Strong positive transcriptomic coordination with CMTM6 (ρ = 0.42, P = 2.3×10⁻⁶⁸), with 74% of correlation persisting after immune adjustment (partial ρ = 0.31, P = 8.7×10⁻³⁸), indicating substantial immune-independent coordination; (2) Negative correlation with STUB1 (ρ = -0.15, P = 6.2×10⁻¹⁰), consistent with its E3 ubiquitin ligase function in PD-L1 degradation, maintaining significance after immune adjustment (partial ρ = -0.12, P = 1.2×10⁻⁶); (3) Robust cross-validation: All transcriptomic associations remained significant across cancer type-specific analyses, outlier exclusion scenarios, bootstrap iterations, and alternative correlation methods, with directional consistency exceeding 95% across sensitivity analyses. Additionally, we demonstrate a proof-of-concept survival analysis framework using simulated outcomes to illustrate how these molecular features could be integrated into multivariable Cox regression models (model C-index=0.72 in simulation).

Conclusions: This multi-dimensional integrative analysis establishes a robust computational framework for dissecting complex regulatory networks in cancer biology. The transcriptomic associations we identify—particularly the immune-independent coordination between PD-L1 and CMTM6, and the negative correlation with STUB1—provide large-scale validation of mechanistic relationships suggested by prior experimental studies. The analytical pipeline developed here, including confounder-adjusted correlation analysis and proof-of-concept survival modeling, provides a generalizable template for investigating molecular regulatory networks across other cancer types and immunotherapy targets.
```

### 作者聲明

**Author Approvals**:
- [x] All authors have approved this submission to bioRxiv
- [x] I understand that submissions are contributions to the scientific record

**Publication Status**:
- [x] This manuscript has not been published by a journal

**Competing Interests**:
- [x] The authors have declared no competing interests

**Funding**:
```
No external funding was received for this work.
```

### 數據和代碼可用性

**Data Availability**:
```
All TCGA expression data are publicly available from the Genomic Data Commons (GDC) Data Portal (https://portal.gdc.cancer.gov/). Sample accession numbers are provided in Supplementary Table S1.
```

**Code Availability**:
```
Complete analysis code and documentation are available at:
https://github.com/thc1006/p62-pdl1-llps-starter

All scripts are provided with detailed instructions for reproducibility.
```

**⚠️ 重要**: 投稿前必須確認 GitHub repository 為**公開狀態**！

### License

**推薦**: ✅ **CC BY 4.0** (Creative Commons Attribution)
- 允許他人分享和改編，需註明出處
- 對學術引用最友好

**備選**: CC BY-NC-ND 4.0（如果您希望限制商業使用和衍生作品）

---

## ⚠️ 投稿前最終確認

### 必須檢查項目

**文件準備**:
- [ ] PDF 可正常打開（在 Adobe Reader 和瀏覽器中測試）
- [ ] 所有圖表清晰顯示
- [ ] 所有表格格式正確
- [ ] 數學公式正確渲染
- [ ] 參考文獻連結可點擊

**GitHub 倉庫**:
- [ ] 倉庫設為公開（Public）
- [ ] README.md 更新完整
- [ ] 代碼有清楚的註解和文檔
- [ ] 測試 URL 可從外部訪問: https://github.com/thc1006/p62-pdl1-llps-starter

**科學誠信**:
- [ ] 模擬數據已在所有相關位置明確標註
- [ ] 未誇大研究發現
- [ ] 限制和注意事項已充分說明
- [ ] 所有數據來源已正確引用

**個人資訊**:
- [ ] Email 地址正確且可接收郵件
- [ ] 機構名稱正確
- [ ] ORCID ID（如有）填寫正確

---

## 🚀 投稿步驟

### Step 1: 前往 bioRxiv
```
https://www.biorxiv.org/submit-a-manuscript
```

### Step 2: 創建帳號（如果還沒有）
- 使用學術 email: hctsai1006@cs.nctu.edu.tw
- 驗證 email 地址

### Step 3: 開始新投稿
- 點擊 "Submit a Manuscript"
- 選擇 "New Submission"

### Step 4: 上傳 PDF
- 上傳 `MANUSCRIPT_bioRxiv_SUBMISSION_FINAL.pdf`
- 等待系統處理（2-3 分鐘）
- 檢查自動提取的 metadata

### Step 5: 填寫 Metadata
按照上方「投稿表單資訊」部分填寫：
1. Title（標題）
2. Authors（作者資訊）
3. Abstract（摘要）- 直接複製貼上
4. Keywords（關鍵詞）
5. Subject Areas（學科領域）
6. Article Type（文章類型）
7. License（授權方式）

### Step 6: 添加補充資訊
- Data availability statement
- Code availability statement
- Funding statement
- Competing interests declaration

### Step 7: 預覽和提交
- 仔細檢查所有資訊
- 預覽格式化後的手稿
- 確認所有聲明
- 點擊 "Submit"

### Step 8: 等待審核
- **篩選時間**: 1-2 個工作日
- **發布時間**: 審核通過後 24-48 小時
- **DOI 分配**: 發布時立即獲得

---

## 📧 投稿後流程

### 確認郵件
✅ 提交確認（立即）
- 確認收到投稿
- 提供投稿編號

⏳ 審核通知（1-2 天）
- 篩選完成通知
- 可能要求修改（通常是格式問題）

🎉 發布通知（2-3 天）
- 手稿已發布
- **DOI 號碼**
- bioRxiv URL

### 獲得 DOI 後

**更新 GitHub README**:
```markdown
## Citation

Tsai HC. (2025). Multi-Dimensional Integrative Analysis of PD-L1
Regulatory Networks: A Computational Framework Integrating Large-Scale
Genomics and Immune Deconvolution Across 1,635 Cancer Patients.
bioRxiv. doi: [您的DOI號碼]
```

**分享 preprint**:
- 在 LinkedIn、ResearchGate、Twitter 分享
- 通知合作者和相關研究者
- 添加到您的 CV 和學術檔案

**準備期刊投稿**（可選）:
- bioRxiv 發布後，可同時或稍後投稿到同行評審期刊
- 大多數期刊接受已發布的 preprints
- 投稿時需註明："This manuscript was previously deposited as a preprint on bioRxiv (DOI: XXX)"

---

## 🎯 建議的後續期刊

### Tier 1: 高影響力計算生物學期刊
- **Bioinformatics** (IF ~6-7)
- **PLOS Computational Biology** (IF ~4-5)
- **BMC Bioinformatics** (IF ~3)

### Tier 2: 癌症生物學期刊
- **Molecular Cancer** (IF ~27, Open Access)
- **Cancer Informatics** (IF ~2-3)
- **npj Precision Oncology** (IF ~5-6)

### Tier 3: 通用科學期刊
- **Scientific Reports** (IF ~4, Nature Publishing)
- **PLOS ONE** (IF ~3)

**注意**: 先投 bioRxiv 不會影響期刊投稿，反而可以：
1. 搶先確立研究優先權
2. 獲得社群反饋
3. 增加論文可見度
4. 累積引用次數

---

## 📞 需要幫助？

### bioRxiv 支援
- 作者指南: https://www.biorxiv.org/submit-a-manuscript
- FAQ: https://www.biorxiv.org/about-biorxiv
- 聯繫: Submit@bioRxiv.org

### 技術問題
如果在投稿過程中遇到：
- PDF 格式問題
- Metadata 提取錯誤
- 檔案上傳失敗

請檢查：
1. PDF 是否由標準工具生成（pdfLaTeX, pandoc）
2. 檔案大小是否 <100 MB
3. 是否包含嵌入字體

---

## ✅ 最終檢查清單（投稿當天）

**投稿前 5 分鐘**:
- [ ] 再次打開 PDF，確認所有內容正確
- [ ] 訪問 GitHub repository，確認為公開狀態
- [ ] 檢查 email 信箱，確保可接收郵件
- [ ] 準備好所有文字內容（Abstract, Keywords）以便複製貼上
- [ ] 深呼吸，準備投稿！

**投稿完成後**:
- [ ] 保存投稿確認郵件
- [ ] 記錄投稿編號
- [ ] 在日曆上標記預期發布日期
- [ ] 準備社群媒體分享文字（等 DOI 發布後使用）

---

## 🎉 恭喜！

您已經完成了一項完整的大規模計算生物學研究！

**研究亮點**:
- ✅ 1,635 個真實 TCGA 樣本
- ✅ 四維整合分析框架
- ✅ 免疫去卷積控制混雜因子
- ✅ 完整的敏感度分析
- ✅ 科學透明度（明確標註模擬數據）
- ✅ 完全可重現（GitHub 開源）

準備好投稿了嗎？**Go for it!** 🚀

---

**文件版本**: 2.0
**最後更新**: 2025-11-08
**下次審查**: 投稿完成後更新狀態
