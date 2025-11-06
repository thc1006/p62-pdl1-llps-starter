# 檔案清理計劃

**分析日期**: 2025-11-06 23:15
**目的**: 整理專案結構，移除過時檔案

---

## 📋 現況分析

### PDF 檔案（根目錄）

| 檔案 | 大小 | 狀態 | 建議 |
|------|------|------|------|
| `MANUSCRIPT_bioRxiv_SUBMISSION_FINAL.pdf` | 2.0 MB | ✅ **最終版本** | **保留 - 這是投稿檔案** |
| `MANUSCRIPT_bioRxiv_SUBMISSION.pdf` | 127 KB | ⚠️ 過時（無圖片版） | 移至 archive/ |
| `MANUSCRIPT_bioRxiv_SUBMISSION_OLD.pdf` | 118 KB | ⚠️ 過時（最早版本） | 移至 archive/ |
| `MANUSCRIPT_bioRxiv_SUBMISSION_WITHTOC.pdf` | 132 KB | ⚠️ 過時（有目錄頁） | 移至 archive/ |

### 文檔檔案（根目錄）

| 檔案 | 大小 | 狀態 | 建議 |
|------|------|------|------|
| `FINAL_PERFECT_SUBMISSION.md` | 5.1 KB | ✅ 最新總結 | **保留** |
| `REAL_FIGURES_UPDATE_REPORT.md` | 6.6 KB | ✅ 圖表報告 | **保留** |
| `SUBMISSION_MATERIALS_COMPLETE.md` | 16 KB | ✅ 材料清單 | **保留** |
| `SUBMISSION_INSTRUCTIONS.md` | 4.0 KB | ✅ 投稿指南 | **保留** |
| `SUPPLEMENTARY_MATERIALS.md` | 20 KB | ✅ 補充材料 | **保留** |
| `PDF_QUALITY_CHECK.md` | 2.1 KB | ✅ 質量檢查 | **保留** |
| `README_PDF_VERSIONS.md` | 768 B | ⚠️ 部分過時 | 更新後保留 |
| `FINAL_SUBMISSION_READY.md` | 6.8 KB | ⚠️ 被更新版取代 | 移至 archive/ |
| `CLAUDE.md` | 11 KB | ℹ️ 開發筆記 | 移至 docs/ |
| `README.md` | 8.2 KB | ⚠️ 需要更新 | 更新投稿狀態 |

---

## 🗂️ 清理行動

### 行動 1: 歸檔過時 PDF
```bash
mkdir -p archive/old_pdfs
mv MANUSCRIPT_bioRxiv_SUBMISSION.pdf archive/old_pdfs/
mv MANUSCRIPT_bioRxiv_SUBMISSION_OLD.pdf archive/old_pdfs/
mv MANUSCRIPT_bioRxiv_SUBMISSION_WITHTOC.pdf archive/old_pdfs/
```

### 行動 2: 歸檔過時文檔
```bash
mkdir -p archive/old_docs
mv FINAL_SUBMISSION_READY.md archive/old_docs/
```

### 行動 3: 整理開發文檔
```bash
mv CLAUDE.md docs/development_notes.md
```

### 行動 4: 更新主要文檔
- 更新 README.md（加入最新投稿狀態）
- 更新 README_PDF_VERSIONS.md（只保留最終版本說明）

### 行動 5: 創建清晰的目錄結構
```
根目錄/
├── MANUSCRIPT_bioRxiv_SUBMISSION_FINAL.pdf  ← 唯一 PDF
├── README.md                                ← 專案說明
├── SUBMISSION_MATERIALS_COMPLETE.md         ← 材料清單
├── FINAL_PERFECT_SUBMISSION.md             ← 投稿總結
├── docs/                                    ← 所有文檔
│   ├── SUBMISSION_INSTRUCTIONS.md
│   ├── PDF_QUALITY_CHECK.md
│   ├── REAL_FIGURES_UPDATE_REPORT.md
│   ├── README_PDF_VERSIONS.md
│   └── development_notes.md
├── archive/                                 ← 歷史檔案
│   ├── old_pdfs/
│   └── old_docs/
└── ...
```

---

## ✅ 預期成果

### 清理後的根目錄
- 1 個 PDF（最終投稿版）
- 3-4 個主要 MD 檔案（README, 投稿總結, 材料清單）
- 清晰的 docs/ 和 archive/ 目錄

### 優點
✅ 一眼就能找到投稿檔案
✅ 不會誤用舊版本 PDF
✅ 歷史檔案保留在 archive/
✅ 文檔分類清楚

