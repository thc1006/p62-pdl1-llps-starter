# bioRxiv 投稿完整指南

**最後更新**: 2025-11-08
**適用手稿**: Multi-Dimensional Integrative Analysis of PD-L1 Regulatory Networks
**準備狀態**: ✅ **完全準備就緒**

---

## 🎯 快速導航

| 章節 | 內容 | 預計時間 |
|------|------|----------|
| [投稿前準備](#-投稿前準備) | 確認所需材料 | 10 分鐘 |
| [bioRxiv 註冊](#-biorxiv-帳號註冊) | 創建或登入帳號 | 5 分鐘 |
| [投稿流程](#-詳細投稿流程) | 逐步填寫表單 | 30 分鐘 |
| [投稿後處理](#-投稿後流程) | 等待與後續步驟 | - |
| [期刊投稿](#-後續期刊投稿建議) | bioRxiv 後的選擇 | - |

**總計投稿時間**: 約 45 分鐘

---

## 🔧 投稿前準備

### 1. 確認手稿完整性

您的手稿已完全準備就緒：

- ✅ **PDF 檔案**: `MANUSCRIPT_bioRxiv_SUBMISSION_FINAL.pdf`
- ✅ **檔案大小**: 2.7 MB（符合 <100 MB 限制）
- ✅ **頁數**: 32 頁
- ✅ **圖表**: 6 張（已嵌入）
- ✅ **表格**: 5 張（已嵌入）
- ✅ **參考文獻**: 完整
- ✅ **模擬數據聲明**: 11 處明確標註

### 2. 準備文字內容（用於複製貼上）

建議打開 `BIORXIV_SUBMISSION_CHECKLIST.md`，其中包含：
- ✅ 完整 Abstract
- ✅ Keywords
- ✅ Data/Code availability statements
- ✅ 所有投稿表單所需文字

### 3. 確認 GitHub Repository 為公開

⚠️ **極度重要**：

```bash
# 訪問您的 repository
https://github.com/thc1006/p62-pdl1-llps-starter

# 必須顯示 "Public" 標籤
```

**如何設為公開**：
1. Settings → Danger Zone → Change visibility
2. 選擇 "Make public"
3. 確認操作

---

## 👤 bioRxiv 帳號註冊

### 如果您已有帳號
- 前往: https://www.biorxiv.org/login
- 輸入 email 和密碼
- 跳到[詳細投稿流程](#-詳細投稿流程)

### 如果需要創建新帳號

#### Step 1: 註冊
訪問: https://www.biorxiv.org/register

填寫資訊：
- **Email**: `hctsai1006@cs.nctu.edu.tw`
- **First Name**: Hsiu-Chi
- **Last Name**: Tsai
- **Institution**: National Yang Ming Chiao Tung University
- **Country**: Taiwan

#### Step 2: 驗證 Email
- 檢查收件匣
- 點擊驗證連結
- 確認帳號激活

---

## 🚀 詳細投稿流程

### 階段 1: 開始投稿

#### Step 1: 登入並開始
1. 訪問 https://www.biorxiv.org/submit-a-manuscript
2. 登入您的帳號
3. 點擊 **"New Submission"**

---

### 階段 2: 上傳 PDF

#### Step 2: 選擇文章類型
- 選擇: **"New Results"**
- 點擊: **"Continue"**

#### Step 3: 上傳手稿
1. 點擊 **"Choose File"**
2. 選擇 `MANUSCRIPT_bioRxiv_SUBMISSION_FINAL.pdf`
3. 等待上傳（1-2 分鐘）
4. 系統自動提取 metadata

---

### 階段 3: 填寫 Metadata

#### Step 4: Title（標題）

**直接複製**：
```
Multi-Dimensional Integrative Analysis of PD-L1 Regulatory Networks: A Computational Framework Integrating Large-Scale Genomics and Immune Deconvolution Across 1,635 Cancer Patients
```

#### Step 5: Authors（作者）

**Corresponding Author**:
- First Name: **Hsiu-Chi**
- Last Name: **Tsai**
- Email: **hctsai1006@cs.nctu.edu.tw**
- Institution: **National Yang Ming Chiao Tung University**
- City: **Hsinchu**
- Country: **Taiwan**
- ORCID: （如有請填寫）

#### Step 6: Abstract（摘要）

**從 BIORXIV_SUBMISSION_CHECKLIST.md 複製完整 Abstract**。

關鍵內容：
- Background: 研究缺口
- Methods: 四維框架，1,635 樣本
- Results: CMTM6-PD-L1 (ρ=0.42), STUB1-PD-L1 (ρ=-0.15)
- Conclusions: 計算框架範本

**提示**: 直接複製貼上，不要手動輸入。

#### Step 7: Keywords（關鍵詞）

```
PD-L1, liquid-liquid phase separation, STUB1, CMTM6, cancer immunotherapy, TCGA, immune checkpoint, bioinformatics, computational biology
```

#### Step 8: Subject Areas（學科領域）

- **Primary**: Bioinformatics
- **Secondary** (如果允許): Cancer Biology

---

### 階段 4: 聲明與授權

#### Step 9: Competing Interests（利益衝突）

選擇：
- ✅ **"The authors have declared no competing interests"**

#### Step 10: Funding（資金）

填寫：
```
No external funding was received for this work.
```

#### Step 11: Author Contributions（貢獻）

**單一作者填寫**：
```
H.C.T. conceived the study, performed all analyses, and wrote the manuscript.
```

#### Step 12: Data Availability（數據可用性）

```
All TCGA expression data are publicly available from the Genomic Data Commons (GDC) Data Portal (https://portal.gdc.cancer.gov/). Complete analysis code and documentation are available at https://github.com/thc1006/p62-pdl1-llps-starter.
```

#### Step 13: Code Availability（代碼可用性）

```
Complete analysis code is available at https://github.com/thc1006/p62-pdl1-llps-starter under an open-source license.
```

#### Step 14: License（授權）

選擇：
- ✅ **CC BY 4.0** (Creative Commons Attribution)

**理由**：
- 允許最大自由度
- 有利於引用和傳播
- 大多數期刊接受

---

### 階段 5: 預覽與提交

#### Step 15: Preview（預覽）

仔細檢查：
- [ ] 標題正確
- [ ] 作者資訊完整
- [ ] Abstract 顯示正確
- [ ] 圖表清晰
- [ ] 參考文獻正確

#### Step 16: 確認聲明

勾選：
- [x] All authors have approved this submission
- [x] I understand submissions are contributions to scientific record
- [x] This manuscript has not been published elsewhere
- [x] I agree to bioRxiv terms and conditions

#### Step 17: 提交

1. 最後檢查所有資訊
2. 深呼吸 🧘
3. 點擊 **"Submit Manuscript"**
4. 確認提交

---

## ✅ 投稿完成！

### 立即收到

1. **確認郵件**（5 分鐘內）
   - 投稿編號
   - 追蹤連結

2. **儀表板更新**
   - 狀態: "Under Review"

---

## ⏰ 投稿後流程

### 時間表

| 時間 | 事件 |
|------|------|
| 0-5 分鐘 | 確認郵件 |
| 1-2 工作日 | 初步審核 |
| 24-48 小時 | 發布（審核通過後） |

### 可能結果

**審核通過** ✅（最常見）
- 等待發布通知
- 獲得 DOI

**要求修改** 📝（偶爾）
- 修正格式問題
- 重新提交

**被拒絕** ❌（罕見）
- 閱讀理由
- 修正後可重投

---

## 🎉 發布後要做的事

### 1. 更新 GitHub

在 `README.md` 添加：

```markdown
[![bioRxiv](https://img.shields.io/badge/bioRxiv-DOI-blue)](https://doi.org/YOUR_DOI)

## Citation
Tsai HC. (2025). Multi-Dimensional Integrative Analysis of PD-L1
Regulatory Networks. bioRxiv. https://doi.org/YOUR_DOI
```

### 2. 分享到社群媒體

**Twitter/X**:
```
🚀 New preprint! Multi-dimensional analysis of PD-L1 regulatory
networks across 1,635 cancer patients.

Key findings:
✅ CMTM6-PD-L1 coordination
✅ STUB1 regulation at scale

📄 [DOI link]

#bioRxiv #CancerResearch #Immunotherapy
```

### 3. 更新學術檔案
- Google Scholar（自動）
- ResearchGate
- ORCID
- CV/Resume

---

## 🎯 後續期刊投稿建議

### 推薦期刊

**Tier 1: 計算生物學**
- Bioinformatics (IF ~6-7, 免費發表)
- PLOS Computational Biology (IF ~4-5)

**Tier 2: 癌症生物學**
- npj Precision Oncology (IF ~5-6)
- Cancer Informatics (IF ~2-3)

**Tier 3: 開放獲取**
- Scientific Reports (IF ~4)
- PLOS ONE (IF ~3)

### 投稿時機

**選項 1**: bioRxiv 發布後立即投期刊
**選項 2**: 等 2-4 週收集反饋再投

**注意**: 95% 期刊接受 preprints

---

## ❓ 常見問題

**Q: bioRxiv 算正式發表嗎？**
A: 不算，但可被引用和列入 CV。

**Q: 發布後還能投期刊嗎？**
A: 可以！大多數期刊接受。

**Q: 需要多久發布？**
A: 通常 2-4 天。

**Q: 可以更新已發布的 preprint 嗎？**
A: 可以，上傳新版本即可。

**Q: GitHub 一定要公開嗎？**
A: 強烈建議，增加可信度。

---

## 📞 需要幫助？

**bioRxiv 支援**:
- Email: submit@biorxiv.org
- FAQ: https://www.biorxiv.org/about-biorxiv

**技術問題**:
- 參考 `BIORXIV_SUBMISSION_CHECKLIST.md`
- 檢查 PDF 格式和大小

---

## ✅ 最終檢查（投稿前 5 分鐘）

- [ ] PDF 可正常打開
- [ ] GitHub repository 為公開
- [ ] Email 可接收郵件
- [ ] 準備好 Abstract 和 Keywords
- [ ] 深呼吸，放鬆！

---

## 🎊 恭喜！

您已經準備好投稿了！

**您的研究亮點**:
- ✅ 1,635 個真實 TCGA 樣本
- ✅ 四維整合框架
- ✅ 免疫去卷積控制
- ✅ 完整敏感度分析
- ✅ 科學透明度
- ✅ 完全可重現

**準備好了嗎？Go for it!** 🚀

---

**文件版本**: 2.0
**最後更新**: 2025-11-08
**維護**: Claude Code Assistant
