# bioRxiv 檔案上傳快速指南

**當前步驟**: 上傳檔案到 bioRxiv

---

## 📁 三個上傳區域

### 1️⃣ Manuscript Files（✅ 必須上傳）

**上傳這個檔案**：

```
檔案名稱: MANUSCRIPT_bioRxiv_SUBMISSION_FINAL.pdf
完整路徑: /home/thc1006/dev/p62-pdl1-llps-starter/MANUSCRIPT_bioRxiv_SUBMISSION_FINAL.pdf
檔案大小: 2.7 MB
```

**如何操作**：
1. 在檔案管理器中打開專案根目錄：`/home/thc1006/dev/p62-pdl1-llps-starter/`
2. 找到檔案：`MANUSCRIPT_bioRxiv_SUBMISSION_FINAL.pdf`
3. 拖曳到 bioRxiv 的 "Drop manuscript Files here" 區域
4. 或點擊 "Select Files" 瀏覽並選擇

---

### 2️⃣ Image Files（⚠️ 可選 - 建議不上傳）

**推薦做法：不上傳**
- ✅ 所有圖片已經嵌入 PDF 中
- ✅ bioRxiv 會自動從 PDF 提取圖片
- ✅ 無需單獨上傳

**如果系統要求上傳圖片**（通常不會）：

圖片位置：
```
目錄: /home/thc1006/dev/p62-pdl1-llps-starter/outputs/figures/
```

可用圖片清單：
```
Figure1_pipeline_flowchart.png      (200 KB)  - 分析流程圖
Figure2_correlations.png            (1.1 MB)  - 相關性分析
Figure3_immune_environment.png      (446 KB)  - 免疫環境
Figure4_survival_analysis.png       (419 KB)  - 生存分析
FigureS1_study_design.png           (302 KB)  - 研究設計
FigureS2_sample_characteristics.png (431 KB)  - 樣本特徵
```

**上傳方式**（如需要）：
1. 打開目錄：`outputs/figures/`
2. 選擇需要的圖片
3. 拖曳到 "Drop image Files here" 區域

---

### 3️⃣ Supplemental Files（⚠️ 可選 - 初次投稿建議不上傳）

**推薦做法：不上傳**
- ✅ 手稿中已說明數據在 GitHub
- ✅ Code Availability 已提供連結
- ✅ bioRxiv 不強制要求補充材料

**如果您想上傳補充材料**：

可用檔案：
```
檔案: SUPPLEMENTARY_MATERIALS.md
位置: /home/thc1006/dev/p62-pdl1-llps-starter/SUPPLEMENTARY_MATERIALS.md
大小: 20 KB
格式: Markdown（需轉為 PDF）
```

**轉換為 PDF**（如需要）：
```bash
# 使用 pandoc 轉換
cd /home/thc1006/dev/p62-pdl1-llps-starter
pandoc SUPPLEMENTARY_MATERIALS.md -o SUPPLEMENTARY_MATERIALS.pdf

# 或使用其他工具
# 1. 打開 .md 檔案
# 2. 複製內容到 Google Docs
# 3. 下載為 PDF
```

---

## ✅ 推薦的上傳方案

### 方案 A：簡單模式（推薦新手）✨

**只上傳主要手稿 PDF**

```
✅ Manuscript Files: MANUSCRIPT_bioRxiv_SUBMISSION_FINAL.pdf (2.7 MB)
❌ Image Files: 不上傳（已嵌入 PDF）
❌ Supplemental Files: 不上傳（GitHub 連結已提供）
```

**理由**：
- PDF 已包含所有圖表
- 代碼和數據在 GitHub 上公開
- bioRxiv 不強制要求補充材料
- 簡化投稿流程

---

### 方案 B：完整模式（如果想提供更多資訊）

```
✅ Manuscript Files: MANUSCRIPT_bioRxiv_SUBMISSION_FINAL.pdf (2.7 MB)
✅ Image Files: 6 張圖片（如果系統要求）
✅ Supplemental Files: SUPPLEMENTARY_MATERIALS.pdf（轉換後）
```

**注意**：此方案需要額外時間處理補充材料。

---

## 🎯 快速檢查清單

上傳前確認：

- [ ] 已找到 `MANUSCRIPT_bioRxiv_SUBMISSION_FINAL.pdf`
- [ ] 檔案大小顯示為 2.7 MB
- [ ] 決定是否上傳圖片（建議：否）
- [ ] 決定是否上傳補充材料（建議：否）

上傳時：

- [ ] 拖曳或選擇主要 PDF
- [ ] 等待上傳完成（約 10-30 秒）
- [ ] 確認檔案已顯示在上傳列表中

---

## 💡 常見問題

**Q: 圖片真的不需要單獨上傳嗎？**
A: 不需要！bioRxiv 會從 PDF 中自動提取圖片。只有當系統明確要求時才上傳。

**Q: 補充材料一定要上傳嗎？**
A: 不一定。您的手稿已在 Data Availability 中提供 GitHub 連結，這已足夠。

**Q: 上傳失敗怎麼辦？**
A: 檢查：
1. 檔案大小是否 <100 MB（您的 2.7 MB 沒問題）
2. 網路連線是否穩定
3. 瀏覽器是否支援（建議 Chrome 或 Firefox）

**Q: 可以稍後補充材料嗎？**
A: 可以！bioRxiv 發布後可以上傳新版本。

---

## 🚀 現在就上傳！

**推薦步驟**：

1. **打開檔案管理器**
   ```
   cd /home/thc1006/dev/p62-pdl1-llps-starter
   ```

2. **找到 PDF**
   - 檔名：`MANUSCRIPT_bioRxiv_SUBMISSION_FINAL.pdf`
   - 大小：2.7 MB

3. **拖曳到 bioRxiv**
   - 目標：Manuscript Files 上傳區

4. **等待處理**
   - 上傳進度條
   - 檔案驗證

5. **繼續填表**
   - 進入下一步（Metadata）

---

**文件版本**: 1.0
**建立日期**: 2025-11-08
**用途**: bioRxiv 投稿檔案上傳指南
