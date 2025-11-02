# SQSTM1 基因別名和映射完整指南

## 官方基因信息

### 主要標識符
| 標識符類型 | 值 |
|-----------|-----|
| **官方基因符號** | SQSTM1 |
| **官方全名** | sequestosome 1 |
| **HGNC ID** | HGNC:11280 |
| **NCBI Gene ID** | 8878 |
| **Ensembl ID** | **ENSG00000161011** |
| **OMIM** | MIM:601530 |
| **UniProt** | Q13501 |
| **染色體位置** | 5q35.3 (chr5:179,806,398-179,838,078) |

---

## 已知別名和替代名稱（完整列表）

### 完整別名清單

| 別名 | 説明 | 備註 |
|-----|------|------|
| **p62** | 最常見的替代名稱 | 蛋白質常用名稱 |
| **A170** | 官方別名 | HGNC 記錄 |
| **OSIL** | 官方別名 | HGNC 記錄 |
| **p60** | 蛋白質相關別名 | 分子量相似 |
| **P62B** | 蛋白質相關別名 | 變體相關 |
| **PDB3** | 官方別名 | 數據庫別名 |
| **ZIP3** | zeta-interacting protein 3 | 功能相關別名 |
| **EBIAP** | EBI3-associated protein | 相互作用蛋白 |
| **DMRV** | 疾病相關別名 | 臨床關聯 |
| **NADGP** | 功能相關別名 | 信號通路相關 |
| **FTDALS3** | FTD and/or ALS 3 | 疾病關聯 |
| **ZIP** | zeta-interacting protein | 簡短形式 |
| **ORCA** | 功能相關別名 | 自噬相關 |

### 蛋白質別名
- **Ubiquitin-binding protein p62** - 完整蛋白質名稱
- **Sequestosome-1** - 正式蛋白質名稱

---

## 外部數據庫識別符

### 各數據庫中的識別符
- **NCBI Gene Database**: 8878
- **Ensembl**: ENSG00000161011
- **HGNC**: HGNC:11280
- **OMIM**: 601530
- **UniProtKB**: Q13501
- **RefSeq Protein**: NP_003891.1, NP_001290254.1
- **RefSeq mRNA**: NM_003900.5

### 主要轉錄本
- **MANE Select Transcript**: ENST00000389805.9 (NM_003900.5)
- **編碼蛋白質**: 440 個氨基酸
- **分子量**: ~47.7 kDa (理論值)
- **轉錄本數**: 26 個(剪接變異)

---

## MyGene.info 查詢指南

### 為什麼 MyGene 可能找不到 SQSTM1？

MyGene.info 通常 **能夠** 找到 SQSTM1，但可能需要：

1. **正確的查詢參數**
   - 使用 `scopes='symbol'` 指定符號查詢
   - 指定 `species='human'` 或 `species=9606`
   - 明確要求 `fields='ensembl.gene'` 包含 Ensembl ID

2. **常見問題**
   - 未指定物種會導致查詢失敗
   - 查詢參數不正確可能返回不完整結果
   - 某些別名在某些版本中可能不被識別
   - 如果查詢參數未正確設置，可能會得到多個結果

3. **API 版本差異**
   - MyGene.info v3.0 和之前版本可能有差異
   - 字段可用性可能因版本而異

---

## Python 查詢代碼示例

### 方法 1: 使用基因符號查詢(推薦)

```python
import mygene

# 初始化 MyGeneInfo 客户端
mg = mygene.MyGeneInfo()

# 方法 A: 使用 querymany() 查詢單個基因(推薦用於映射)
result = mg.querymany(['SQSTM1'],
                      scopes='symbol',
                      species='human',
                      fields='ensembl.gene,symbol,entrezgene,refseq,uniprot',
                      verbose=True)

# 查看結果
for item in result:
    print(f"Symbol: {item['symbol']}")
    print(f"Entrez Gene ID: {item['entrezgene']}")
    print(f"Ensembl ID: {item['ensembl']['gene']}")
    print(f"UniProt: {item.get('uniprot', {})}")
    print(f"RefSeq: {item.get('refseq', {})}")
```

### 方法 2: 使用 Ensembl ID 直接查詢

```python
import mygene

mg = mygene.MyGeneInfo()

# 直接用 Ensembl ID 查詢
result = mg.getgene('ENSG00000161011',
                     fields='symbol,ensembl,entrezgene,name')

print(f"Symbol: {result['symbol']}")
print(f"Gene Name: {result['name']}")
print(f"Entrez ID: {result['entrezgene']}")
print(f"Ensembl ID: {result['ensembl']['gene']}")
```

### 方法 3: 使用 Entrez Gene ID 查詢

```python
import mygene

mg = mygene.MyGeneInfo()

# 使用 Entrez Gene ID 查詢
result = mg.getgene(8878,
                     fields='symbol,ensembl.gene,name,entrezgene')

print(f"Symbol: {result['symbol']}")
print(f"Ensembl ID: {result['ensembl']['gene']}")
print(f"Full Name: {result['name']}")
```

### 方法 4: 批量查詢多個基因

```python
import mygene
import pandas as pd

mg = mygene.MyGeneInfo()

# 批量查詢多個基因(包括別名)
genes = ['SQSTM1', 'p62', 'CDK2', 'TP53']  # p62 是 SQSTM1 的別名

results = mg.querymany(genes,
                       scopes='symbol',
                       species='human',
                       fields='ensembl.gene,symbol,entrezgene',
                       as_dataframe=True)  # 轉換為 pandas DataFrame

print(results)
```

### 方法 5: 別名查詢(測試哪些別名有效)

```python
import mygene

mg = mygene.MyGeneInfo()

# 別名列表
aliases = ['SQSTM1', 'p62', 'A170', 'OSIL', 'PDB3', 'ZIP3', 'EBIAP']

for alias in aliases:
    try:
        result = mg.query(f'symbol:{alias}', species='human', size=1)
        if result['total'] > 0:
            hit = result['hits'][0]
            print(f"{alias:10} -> Symbol: {hit.get('symbol', 'N/A'):10} "
                  f"Ensembl: {hit.get('ensembl', {}).get('gene', 'N/A')}")
        else:
            print(f"{alias:10} -> NOT FOUND")
    except Exception as e:
        print(f"{alias:10} -> ERROR: {str(e)}")
```

### 方法 6: 通過 REST API 直接查詢(HTTP)

```python
import requests
import json

# 查詢方法 1: 按基因符號
url = "http://mygene.info/v3/query?q=symbol:SQSTM1&species=human&fields=ensembl.gene,symbol,entrezgene"
response = requests.get(url)
data = response.json()
print(json.dumps(data, indent=2))

# 查詢方法 2: 按 Ensembl ID
url = "http://mygene.info/v3/gene/ENSG00000161011?fields=symbol,ensembl.gene,entrezgene"
response = requests.get(url)
data = response.json()
print(json.dumps(data, indent=2))

# 查詢方法 3: 批量查詢
url = "http://mygene.info/v3/query"
payload = {
    'q': ['SQSTM1', 'p62', 'CDK2'],
    'scopes': 'symbol',
    'species': 'human',
    'fields': 'ensembl.gene,symbol,entrezgene'
}
response = requests.post(url, json=payload)
data = response.json()
for item in data:
    print(f"{item['_id']} -> {item.get('symbol', 'N/A')}")
```

---

## 完整的多功能查詢函數

```python
import mygene
from typing import Union, List, Dict, Optional

class SQSTM1QueryHandler:
    """SQSTM1 基因查詢處理器"""

    def __init__(self):
        self.mg = mygene.MyGeneInfo()
        self.gene_symbol = 'SQSTM1'
        self.entrez_id = 8878
        self.ensembl_id = 'ENSG00000161011'
        self.aliases = ['SQSTM1', 'p62', 'A170', 'OSIL', 'PDB3', 'ZIP3', 'EBIAP', 'DMRV', 'NADGP', 'FTDALS3']

    def get_by_symbol(self, symbol: str = 'SQSTM1') -> Dict:
        """通過基因符號查詢"""
        results = self.mg.querymany([symbol],
                                    scopes='symbol',
                                    species='human',
                                    fields='ensembl.gene,symbol,entrezgene,name,uniprot,refseq')
        return results[0] if results else None

    def get_by_ensembl(self, ensembl_id: str = 'ENSG00000161011') -> Dict:
        """通過 Ensembl ID 查詢"""
        return self.mg.getgene(ensembl_id,
                               fields='symbol,ensembl.gene,entrezgene,name,uniprot')

    def get_by_entrez(self, entrez_id: int = 8878) -> Dict:
        """通過 Entrez Gene ID 查詢"""
        return self.mg.getgene(entrez_id,
                               fields='symbol,ensembl.gene,name,uniprot')

    def test_all_aliases(self) -> Dict[str, bool]:
        """測試所有已知別名"""
        results = {}
        for alias in self.aliases:
            try:
                result = self.mg.query(f'symbol:{alias}', species='human', size=1)
                results[alias] = result['total'] > 0
            except:
                results[alias] = False
        return results

    def get_mapping_info(self) -> Dict:
        """獲取完整的映射信息"""
        data = self.get_by_symbol()
        if data:
            return {
                'symbol': data.get('symbol'),
                'gene_name': data.get('name'),
                'entrez_id': data.get('entrezgene'),
                'ensembl_id': data.get('ensembl', {}).get('gene'),
                'uniprot_id': data.get('uniprot'),
                'refseq': data.get('refseq')
            }
        return None

# 使用示例
handler = SQSTM1QueryHandler()

print("=== 基因映射信息 ===")
mapping = handler.get_mapping_info()
for key, value in mapping.items():
    print(f"{key:15}: {value}")

print("\n=== 別名測試 ===")
alias_results = handler.test_all_aliases()
for alias, found in alias_results.items():
    status = "FOUND" if found else "NOT FOUND"
    print(f"{alias:10}: {status}")

print("\n=== Ensembl 直接查詢 ===")
ensembl_data = handler.get_by_ensembl()
print(f"Symbol: {ensembl_data['symbol']}")
print(f"Ensembl ID: {ensembl_data['ensembl']['gene']}")
```

---

## 重要提示

### 1. 為什麼使用 ENSG00000161011 而非別名
- **ENSG00000161011** 是官方的 Ensembl 基因 ID，國際認可
- 別名(如 p62)可能在不同數據庫版本中有不同對應
- 當做精確映射時，應使用官方標識符

### 2. MyGene.info 的限制
- 別名支持因數據庫版本而異
- 某些別名可能在某些查詢中返回多個結果
- 建議始終指定 `species='human'` 以避免混淆

### 3. 推薦的查詢順序
1. 首先用官方符號 **SQSTM1** 查詢
2. 如果失敗，用 **Ensembl ID** ENSG00000161011
3. 如果失敗，用 **Entrez ID** 8878
4. 最後才嘗試別名(如 p62)

### 4. 跨物種注意事項
- 小鼠同源基因: **Sqstm1** (MGI:107931)
- 斑馬魚同源基因: sqstm1 (ZDB-GENE-040426-2204)
- 查詢時需明確指定 `species` 參數

---

## 參考資源

### 官方數據庫鏈接
- NCBI Gene: https://www.ncbi.nlm.nih.gov/gene/8878
- Ensembl: https://www.ensembl.org/Homo_sapiens/Gene/Summary?g=ENSG00000161011
- HGNC: https://www.genenames.org/data/gene-symbol-report/#!/hgnc_id/HGNC:11280
- OMIM: https://omim.org/entry/601530
- UniProt: https://www.uniprot.org/uniprot/Q13501

### 查詢工具
- MyGene.info: https://mygene.info/
- MyGene.py 文檔: https://docs.mygene.info/
- GeneCards: https://www.genecards.org/cgi-bin/carddisp.pl?gene=SQSTM1

### 相關文獻
- p62/SQSTM1 在自噬中的角色研究
- SQSTM1 在代謝和信號傳導中的功能
- SQSTM1 突變與帕傑特病和額顳葉癡呆的關聯

---

## 快速參考表

| 任務 | 推薦方法 | 代碼 |
|-----|--------|------|
| 查詢基因信息 | `querymany` + 符號 | `mg.querymany(['SQSTM1'], scopes='symbol', species='human')` |
| 獲取 Ensembl ID | `getgene` + Ensembl ID | `mg.getgene('ENSG00000161011')` |
| 批量映射 | `querymany` + DataFrame | `mg.querymany(genes, scopes='symbol', as_dataframe=True)` |
| 測試別名 | `query` + 符號前綴 | `mg.query('symbol:p62', species='human')` |
| REST API 查詢 | HTTP GET/POST | `requests.get("http://mygene.info/v3/...")` |

---

*最後更新: 2025年11月*
*信息來源: NCBI, Ensembl, HGNC, MyGene.info 官方數據庫*
