# Figure 1 最終修復報告

**日期:** 2025-11-07 13:25
**狀態:** ✅ 完全修復

---

## 問題診斷（基於視覺分析）

### 原始問題：

1. **Module 3 (Statistical Analysis) 三個橘色框內文字完全混亂：**
   - ❌ 左框：文字堆疊 "Correlation *Spearman* ρ = Partial..."
   - ❌ 中框：文字超出邊框 "6covariates ρ = 0.3..."
   - ❌ 右框：文字堆疊 "Survival *Cox Model* 0.72 C-index"
   - ❌ 關鍵數據（ρ = 0.42, CD274-CMTM6, 74% retained）未正確顯示

2. **Module 4 (Sensitivity Validation)：**
   - ❌ 文字超出底部邊框

3. **整體佈局：**
   - ❌ 文字橫向溢出而非垂直排列

### 根本原因：

之前的 TikZ 代碼問題：
```latex
% 錯誤的寫法：使用 tabular 環境在 node 內
\node[anchor=center, font=\small] at (trackA.center) {
    \begin{tabular}{c}
    {\Large\bfseries Correlation} \\[8pt]
    \textit{Spearman} \\[8pt]
    {\huge\bfseries\color{analysiscolor!90!black} $\rho = 0.42$} \\[6pt]
    {\normalsize CD274-CMTM6}
    \end{tabular}
};
```

**問題：**
- `tabular` 環境與 `text width` 衝突
- `anchor=center` 使用分離的 node 導致定位錯誤
- 字體大小 (`\huge`) 超出預設的 `text width`

---

## 解決方案

### 新的 TikZ 設計原則：

1. **直接在 node 內使用簡單的 LaTeX 命令，不用 tabular**
2. **統一使用 node 內容，不分離 anchor**
3. **調整字體大小以適應 text width**

### 修復後的代碼：

```latex
\tikzstyle{trackbox} = [
    rectangle,
    rounded corners=4pt,
    minimum width=3.5cm,
    text width=3.2cm,           % 明確限制文字寬度
    minimum height=2.8cm,        % 增加高度容納所有內容
    align=center,                % 文字居中對齊
    draw=black,
    line width=1.2pt,
    drop shadow={opacity=0.3},
    fill=white
]

% Track A - Correlation (正確的寫法)
\node[trackbox, draw=analysiscolor, below=0.7cm of module3title, xshift=-4.3cm] (trackA) {
    {\large\bfseries Correlation}\\[6pt]       % 標題
    {\small\itshape Spearman}\\[6pt]           % 方法
    {\LARGE\bfseries\color{analysiscolor!90!black} $\rho = 0.42$}\\[6pt]  % 數值
    {\footnotesize CD274-CMTM6}                % 說明
};
```

### 關鍵改進：

1. ✅ **text width=3.2cm**：確保文字不超出 3.5cm 的框
2. ✅ **minimum height=2.8cm**：增加高度以容納4行內容
3. ✅ **align=center**：TikZ 原生的居中對齊
4. ✅ **直接使用 `\\[6pt]` 換行**：不依賴 tabular
5. ✅ **字體大小調整**：`\LARGE` 取代 `\huge`

---

## 修復結果對比

### Module 3 - Statistical Analysis (三個框)

| 框 | 修復前 | 修復後 |
|---|--------|--------|
| **左框 (Correlation)** | ❌ 文字堆疊混亂 | ✅ Correlation<br>Spearman<br>ρ = 0.42<br>CD274-CMTM6 |
| **中框 (Partial)** | ❌ 文字超出邊框 | ✅ Partial<br>6 covariates<br>ρ = 0.31<br>74% retained |
| **右框 (Survival)** | ❌ 數字堆疊 | ✅ Survival<br>Cox Model<br>0.72<br>C-index |

### Module 4 - Sensitivity Validation

| 元素 | 修復前 | 修復後 |
|------|--------|--------|
| **文字顯示** | ❌ 超出底部邊框 | ✅ 完整顯示在邊框內 |
| **內容** | 部分被截斷 | ✅ Bootstrap (1,000) • Outlier tests • Stratification<br>LUAD (n=601) — LUSC (n=562) — SKCM (n=472)<br>Consistency >95% across all tests |

---

## 技術細節

### TikZ 完整代碼位置：
`/home/thc1006/dev/p62-pdl1-llps-starter/scripts/figure_generation/tikz/figure1_tikz.tex`

### 生成流程：

1. **編譯 TikZ → PDF：**
   ```bash
   cd scripts/figure_generation/tikz
   pdflatex -interaction=nonstopmode figure1_tikz.tex
   ```
   輸出：`figure1_tikz.pdf` (88 KB)

2. **轉換 PDF → PNG (300 DPI)：**
   ```bash
   pdftoppm figure1_tikz.pdf outputs/figures/Figure1_pipeline_flowchart -png -singlefile -r 300
   ```
   輸出：`outputs/figures/Figure1_pipeline_flowchart.png` (204 KB)

3. **重新生成最終 PDF：**
   ```bash
   pandoc paper/MANUSCRIPT_bioRxiv_FOR_PDFLATEX.md \
       -o MANUSCRIPT_bioRxiv_SUBMISSION_FINAL.pdf \
       --pdf-engine=pdflatex \
       --resource-path=.:paper:outputs/figures
   ```
   輸出：`MANUSCRIPT_bioRxiv_SUBMISSION_FINAL.pdf` (2.7 MB, 32 pages)

---

## 視覺驗證

### 修復前的問題截圖（從用戶描述）：
- Track A-C 的文字完全混亂
- 數值無法辨識
- 框內文字互相重疊

### 修復後確認：
✅ **Track A:** 清晰顯示 "Correlation / Spearman / ρ = 0.42 / CD274-CMTM6"
✅ **Track B:** 清晰顯示 "Partial / 6 covariates / ρ = 0.31 / 74% retained"
✅ **Track C:** 清晰顯示 "Survival / Cox Model / 0.72 / C-index"
✅ **Module 4:** 所有文字完整顯示在邊框內
✅ **整體佈局:** 專業、整潔、易讀

---

## 最終輸出

### 文件：
- ✅ `MANUSCRIPT_bioRxiv_SUBMISSION_FINAL.pdf` (2.7 MB, 32 pages)
- ✅ `outputs/figures/Figure1_pipeline_flowchart.png` (204 KB, 300 DPI)
- ✅ `scripts/figure_generation/tikz/figure1_tikz.pdf` (88 KB)

### 狀態：
**🎉 完全修復，可直接用於 bioRxiv 投稿**

### 投稿清單：
參見 `BIORXIV_SUBMISSION_CHECKLIST.md`

---

**修復完成時間:** 2025-11-07 13:25 UTC
**總修復時間:** ~10 分鐘
**問題嚴重程度:** 高（影響圖表可讀性）
**修復狀態:** ✅ 完全解決
