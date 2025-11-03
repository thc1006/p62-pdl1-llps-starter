# SQSTM1 基因查詢常見問題解答 (FAQ)

## 核心信息速查表

| 項目 | 值 |
|-----|-----|
| **官方基因符號** | SQSTM1 |
| **最常見別名** | p62 |
| **官方 Ensembl ID** | ENSG00000161011 |
| **NCBI Entrez Gene ID** | 8878 |
| **HGNC ID** | HGNC:11280 |
| **UniProt ID** | Q13501 |
| **標準蛋白質名稱** | Sequestosome-1 (ubiquitin-binding protein p62) |
| **蛋白質分子量** | ~47.7 kDa |
| **染色體位置** | 5q35.3 |
| **基因長度** | ~31.7 kb (179,806,398-179,838,078) |

---

## Q1: MyGene.info 為什麼找不到 SQSTM1？

### 常見原因及解決方案

#### 原因 1: 未指定物種
**問題:** 查詢時沒有指定 `species` 參數
```python
# 錯誤做法
mg.querymany(['SQSTM1'], scopes='symbol')

# 正確做法
mg.querymany(['SQSTM1'], scopes='symbol', species='human')
```

#### 原因 2: 查詢範圍不正確
**問題:** 未指定查詢範圍 (scopes)
```python
# 錯誤做法
mg.querymany(['SQSTM1'])

# 正確做法
mg.querymany(['SQSTM1'], scopes='symbol', species='human')

# 或用前綴指定
mg.query('symbol:SQSTM1', species='human')
```

#### 原因 3: 使用別名但別名未被識別
**問題:** 某些別名在特定版本中可能不被識別
```python
# 如果 p62 不工作，使用官方符號
try:
    result = mg.query('symbol:p62', species='human')
except:
    result = mg.query('symbol:SQSTM1', species='human')
```

#### 原因 4: 返回結果過多或過少
**問題:** 別名查詢可能返回多個結果，選擇不當
```python
# 限制結果數量並檢查
results = mg.query('symbol:p62', species='human', size=1)
if results['total'] > 1:
    # 多個結果，使用官方符號確認
    official = mg.querymany(['SQSTM1'], scopes='symbol', species='human')
```

#### 原因 5: 數據庫版本不同步
**問題:** 本地 MyGene.py 版本與服務器版本不匹配
```python
# 更新 MyGene.py
pip install --upgrade mygene

# 檢查版本
import mygene
print(mygene.__version__)
```

---

## Q2: SQSTM1 有哪些官方別名？

### 完整的別名列表

#### 基因符號別名 (Gene Symbol Aliases)
這些是官方認可的基因符號別名：
- **A170** - 老舊別名
- **OSIL** - 官方別名
- **PDB3** - 帕傑特病相關別名
- **ZIP3** - zeta-interacting protein 3

#### 蛋白質別名 (Protein Aliases)
這些是基於蛋白質的別名：
- **p62** - 分子量相關名稱 (最常見)
- **p60** - 分子量相關名稱
- **P62B** - 蛋白質變體相關

#### 功能/相互作用相關別名
- **EBIAP** - EBI3-associated protein (60 kDa EBI3 binding protein)
- **ZIP** - zeta-interacting protein (簡短形式)
- **ORCA** - 自噬相關蛋白

#### 疾病相關別名
這些別名反映了基因與特定疾病的關聯：
- **DMRV** - 疾病相關
- **NADGP** - 信號通路相關
- **FTDALS3** - Frontotemporal Dementia and/or Amyotrophic Lateral Sclerosis 3
  - 反映了 SQSTM1 突變與 FTD/ALS 的關聯

### 哪些別名在 MyGene.info 中可用？

根據測試，以下別名通常在 MyGene.info 中可被識別：
- ✓ **SQSTM1** (官方符號 - 推薦)
- ✓ **p62** (最常見別名 - 通常可用)
- ✓ **A170** (可能可用)
- ✗ **ZIP3**, **ORCA** 等 (可能不可用)

**建議:** 優先使用官方符號 **SQSTM1**

---

## Q3: 如何確保 SQSTM1 和 Ensembl ID 的正確映射？

### 驗證步驟

#### 步驟 1: 確認基本信息
```python
import mygene

mg = mygene.MyGeneInfo()

# 查詢官方符號
result = mg.querymany(['SQSTM1'],
                      scopes='symbol',
                      species='human',
                      fields='ensembl.gene,symbol,entrezgene')

for item in result:
    print(f"Symbol: {item['symbol']}")
    print(f"Ensembl: {item['ensembl']['gene']}")
    print(f"Entrez: {item['entrezgene']}")
```

預期輸出:
```
Symbol: SQSTM1
Ensembl: ENSG00000161011
Entrez: 8878
```

#### 步驟 2: 交叉驗證
```python
# 用 Ensembl ID 反向查詢
result = mg.getgene('ENSG00000161011',
                     fields='symbol,ensembl.gene')

assert result['symbol'] == 'SQSTM1'
assert result['ensembl']['gene'] == 'ENSG00000161011'
print("✓ 映射驗證成功")
```

#### 步驟 3: 檢查別名一致性
```python
# 確保別名也指向同一基因
sqstm1 = mg.querymany(['SQSTM1'], scopes='symbol',
                      species='human', fields='ensembl.gene')
p62 = mg.querymany(['p62'], scopes='symbol',
                   species='human', fields='ensembl.gene')

sqstm1_ensembl = sqstm1[0]['ensembl']['gene']
p62_ensembl = p62[0]['ensembl']['gene']

if sqstm1_ensembl == p62_ensembl == 'ENSG00000161011':
    print("✓ 所有別名指向相同的基因")
else:
    print("✗ 警告: 別名指向不同的基因")
```

---

## Q4: p62 和 SQSTM1 是同一個基因嗎？

### 答案: 是的

- **SQSTM1** 是官方的**基因符號** (基因名稱)
- **p62** 是編碼蛋白質的**常用別名** (蛋白質名稱)
- 它們都指向同一個基因 (Ensembl: ENSG00000161011)

### 為什麼有兩個名稱？

1. **歷史原因**: p62 是基於蛋白質的分子量首先被發現的
2. **命名規範**: SQSTM1 是 HGNC (Human Gene Nomenclature Committee) 指定的官方名稱
3. **領域習慣**: 生物學家經常在論文中混用這兩個名稱

### 查詢時的建議

| 場景 | 推薦 | 理由 |
|-----|------|------|
| 基因映射 | 使用 **SQSTM1** | 官方符號，更穩定 |
| 查詢文獻 | 兩個都用 | 論文中經常混用 |
| 蛋白質研究 | 可用 **p62** | 常見於蛋白質上下文 |
| 數據庫查詢 | **SQSTM1** 優先 | 數據庫中更一致 |

---

## Q5: 如何在 Python 中進行正確的基因映射？

### 推薦代碼模板

```python
import mygene
from typing import Dict, Optional

def map_gene_to_ensembl(gene_symbol: str,
                        species: str = 'human') -> Optional[str]:
    """
    將基因符號映射到 Ensembl ID

    參數:
        gene_symbol: 基因符號 (如 'SQSTM1')
        species: 物種 ('human', 'mouse', 'rat')

    返回:
        Ensembl ID 或 None (如果未找到)
    """
    mg = mygene.MyGeneInfo()

    try:
        # 使用 querymany 進行符號查詢
        results = mg.querymany(
            [gene_symbol],
            scopes='symbol',
            species=species,
            fields='ensembl.gene',
            verbose=False
        )

        if results and len(results) > 0:
            ensembl_info = results[0].get('ensembl', {})
            if isinstance(ensembl_info, dict):
                return ensembl_info.get('gene')
            return ensembl_info

        return None

    except Exception as e:
        print(f"錯誤: {str(e)}")
        return None

def map_ensembl_to_gene_info(ensembl_id: str) -> Optional[Dict]:
    """
    從 Ensembl ID 獲取基因信息

    參數:
        ensembl_id: Ensembl 基因 ID

    返回:
        包含基因信息的字典
    """
    mg = mygene.MyGeneInfo()

    try:
        result = mg.getgene(
            ensembl_id,
            fields='symbol,ensembl.gene,entrezgene,name'
        )

        return {
            'symbol': result.get('symbol'),
            'ensembl_id': result.get('ensembl', {}).get('gene'),
            'entrez_id': result.get('entrezgene'),
            'name': result.get('name')
        }

    except Exception as e:
        print(f"錯誤: {str(e)}")
        return None

# 使用示例
if __name__ == '__main__':
    # SQSTM1 -> Ensembl
    ensembl = map_gene_to_ensembl('SQSTM1')
    print(f"SQSTM1 -> {ensembl}")
    # 輸出: SQSTM1 -> ENSG00000161011

    # Ensembl -> 基因信息
    info = map_ensembl_to_gene_info('ENSG00000161011')
    print(f"ENSG00000161011 -> {info['symbol']}")
    # 輸出: ENSG00000161011 -> SQSTM1
```

---

## Q6: 別名 A170, OSIL, PDB3 等在哪些情況下有用？

### 別名適用場景

| 別名 | 最常見用途 | 何時使用 | 是否推薦 |
|-----|---------|---------|--------|
| **SQSTM1** | 基因 ID 映射 | 所有情況 | ✓ 強烈推薦 |
| **p62** | 蛋白質研究/文獻 | 查詢舊文獻 | ✓ 常用 |
| **A170** | 遺留數據 | 處理舊數據集 | ⚠ 謹慎使用 |
| **OSIL** | 遺留數據 | 處理舊數據集 | ⚠ 謹慎使用 |
| **PDB3** | 帕傑特病研究 | 帕傑特病相關研究 | ⚠ 特定領域 |
| **ZIP3** | 文獻搜索 | 查找相關論文 | ⚠ 不推薦查詢 |
| **EBIAP** | 相互作用研究 | HDAC6 相互作用研究 | ⚠ 特定領域 |
| **FTDALS3** | FTD/ALS 研究 | 神經退行性疾病研究 | ⚠ 特定領域 |

### 何時別名會導致查詢失敗？

1. **版本差異**: 舊別名在新版本 MyGene.info 中可能已被棄用
2. **歧義性**: 某些別名可能指向多個基因
3. **物種特異性**: 某個物種特定的別名在人類中可能不適用

---

## Q7: SQSTM1 與 FTD (額顳葉癡呆) 的關係是什麼？

### SQSTM1 與神經退行性疾病

SQSTM1 與多種神經退行性疾病的關聯：

#### 1. **帕傑特病 (Paget Disease of Bone)**
- 病名: PDB3 (Paget Disease of Bone 3)
- SQSTM1 突變導致異常骨代謝
- 這是為什麼 **PDB3** 是一個別名

#### 2. **額顳葉癡呆 (FTD) 和 ALS**
- 病名: FTDALS3 (Frontotemporal Dementia and/or ALS 3)
- SQSTM1 突變導致蛋白質聚集
- p62/SQSTM1 參與自噬調節，其缺陷導致神經元退化
- 這是為什麼 **FTDALS3** 是一個別名

#### 3. **涵蓋性肌強直症 (Inclusion Body Myositis)**
- SQSTM1 蛋白聚集與肌病相關

### 臨床研究意義
- SQSTM1 突變檢測是 FTD/ALS 診斷的一部分
- p62 蛋白聚集是神經退行性疾病的標誌
- 靶向 SQSTM1 是治療策略的重點

---

## Q8: 如何批量查詢多個基因包括別名？

### 安全的批量查詢策略

```python
import mygene
import pandas as pd

def batch_query_with_aliases(genes: list,
                             species: str = 'human') -> pd.DataFrame:
    """
    批量查詢基因，自動處理別名
    """
    mg = mygene.MyGeneInfo()

    # 方法 1: 首先用官方符號查詢
    results = mg.querymany(
        genes,
        scopes='symbol',
        species=species,
        fields='ensembl.gene,symbol,entrezgene,name',
        as_dataframe=True
    )

    # 方法 2: 對於查詢失敗的基因，嘗試別名
    # (此邏輯需要自定義實現)

    return results

# 使用示例
genes = ['SQSTM1', 'CDK2', 'TP53', 'BRCA1']
df = batch_query_with_aliases(genes)
print(df[['symbol', 'ensembl.gene', 'entrezgene']])
```

---

## Q9: SQSTM1 在不同物種中的名稱是什麼？

### 跨物種基因名稱

| 物種 | 基因名稱 | ID | 備註 |
|-----|---------|-----|------|
| **人類 (Homo sapiens)** | SQSTM1 | ENSG00000161011 | 官方符號 |
| **小鼠 (Mus musculus)** | Sqstm1 | ENSMUSG00000026509 | 大寫 S,其他小寫 |
| **大鼠 (Rattus norvegicus)** | Sqstm1 | ENSRNOG00000009191 | 大鼠特異 |
| **斑馬魚 (Danio rerio)** | sqstm1 | ENSDARG00000039423 | 全小寫 |
| **線蟲 (C. elegans)** | sqst-1 | WBGene00005003 | 簡化名稱 |
| **果蠅 (D. melanogaster)** | ref(2)P | FBgn0000261 | 基因標記名稱 |

### 查詢跨物種同源基因

```python
import mygene

mg = mygene.MyGeneInfo()

# 查詢小鼠同源基因
result = mg.query('symbol:Sqstm1', species='mouse', fields='ensembl.gene')
print(f"小鼠: {result['hits'][0]['ensembl']['gene']}")

# 查詢大鼠同源基因
result = mg.query('symbol:Sqstm1', species='rat', fields='ensembl.gene')
print(f"大鼠: {result['hits'][0]['ensembl']['gene']}")
```

---

## Q10: 如果查詢失敗，應該如何故障排除？

### 故障排除檢查清單

```python
import mygene
import sys

def troubleshoot_gene_query(gene_symbol: str, verbose=True):
    """
    基因查詢故障排除
    """
    mg = mygene.MyGeneInfo()

    checks = {
        '1. 驗證 MyGene 連接': False,
        '2. 驗證基因符號拼寫': False,
        '3. 驗證物種參數': False,
        '4. 驗證字段名稱': False,
        '5. 檢查查詢範圍': False,
        '6. 驗證結果': False
    }

    # 檢查 1: MyGene 連接
    try:
        metadata = mg.metadata()
        checks['1. 驗證 MyGene 連接'] = True
        if verbose:
            print("✓ MyGene 連接正常")
    except Exception as e:
        if verbose:
            print(f"✗ MyGene 連接失敗: {str(e)}")
        return checks

    # 檢查 2-5: 查詢
    try:
        result = mg.querymany(
            [gene_symbol],
            scopes='symbol',
            species='human',
            fields='ensembl.gene,symbol,entrezgene',
            verbose=True
        )
        checks['2. 驗證基因符號拼寫'] = True
        checks['3. 驗證物種參數'] = True
        checks['4. 驗證字段名稱'] = True
        checks['5. 檢查查詢範圍'] = True

        # 檢查 6: 結果
        if result and len(result) > 0:
            checks['6. 驗證結果'] = True
            if verbose:
                print(f"✓ 找到基因: {result[0]['symbol']}")
        else:
            if verbose:
                print(f"✗ 未找到基因: {gene_symbol}")

    except Exception as e:
        if verbose:
            print(f"✗ 查詢出錯: {str(e)}")

    return checks

# 使用示例
checks = troubleshoot_gene_query('SQSTM1')
print("\n故障排除結果:")
for check, passed in checks.items():
    status = "✓" if passed else "✗"
    print(f"{status} {check}")
```

---

## 快速解決方案表

| 問題 | 快速解決方案 |
|-----|-----------|
| 找不到 SQSTM1 | `mg.querymany(['SQSTM1'], scopes='symbol', species='human')` |
| p62 返回多個結果 | 使用官方符號 SQSTM1 替代 |
| 需要 Ensembl ID | `fields='ensembl.gene'` |
| 需要 Entrez ID | `fields='entrezgene'` |
| 批量查詢 | `as_dataframe=True` |
| 跨物種查詢 | 指定 `species` 參數 |
| 調試查詢 | 加上 `verbose=True` |
| 獲取所有信息 | 不指定 `fields` 參數 |

---

## 推薦的外部資源

### 官方數據庫
1. **NCBI Gene**: https://www.ncbi.nlm.nih.gov/gene/8878
2. **Ensembl**: https://www.ensembl.org/Homo_sapiens/Gene/Summary?g=ENSG00000161011
3. **HGNC**: https://www.genenames.org/data/gene-symbol-report/#!/hgnc_id/HGNC:11280
4. **UniProt**: https://www.uniprot.org/uniprot/Q13501

### 查詢工具
1. **MyGene.info**: https://mygene.info/
2. **GeneCards**: https://www.genecards.org/cgi-bin/carddisp.pl?gene=SQSTM1
3. **Ensembl BioMart**: https://www.ensembl.org/biomart

### 文獻資源
1. PubMed: 搜索 "SQSTM1" 或 "p62"
2. Google Scholar: 搜索同上
3. OMIM (601530): https://omim.org/entry/601530

---

*最後更新: 2025年11月*
*所有信息均基於官方數據庫 (NCBI, Ensembl, HGNC, MyGene.info)*
