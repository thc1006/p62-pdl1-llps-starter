#!/usr/bin/env python3
"""
SQSTM1 基因查詢和映射工具

此腳本提供多種方法查詢 SQSTM1 基因信息，包括：
- 通過官方基因符號查詢
- 通過 Ensembl ID 查詢
- 通過 Entrez Gene ID 查詢
- 測試所有已知別名
- 批量映射多個基因
"""

import mygene
import json
from typing import Dict, List, Optional, Union
import sys

# SQSTM1 基因信息常數
SQSTM1_INFO = {
    'symbol': 'SQSTM1',
    'ensembl_id': 'ENSG00000161011',
    'entrez_id': 8878,
    'hgnc_id': 'HGNC:11280',
    'uniprot_id': 'Q13501',
    'aliases': [
        'SQSTM1',      # 官方符號
        'p62',         # 最常見的替代名稱
        'A170',        # 官方別名
        'OSIL',        # 官方別名
        'p60',         # 蛋白質相關別名
        'P62B',        # 蛋白質相關別名
        'PDB3',        # 官方別名
        'ZIP3',        # zeta-interacting protein 3
        'EBIAP',       # EBI3-associated protein
        'DMRV',        # 疾病相關別名
        'NADGP',       # 功能相關別名
        'FTDALS3',     # FTD and/or ALS 3
        'ZIP',         # zeta-interacting protein
        'ORCA',        # 自噬相關別名
    ]
}


class SQSTM1Querier:
    """SQSTM1 基因查詢類"""

    def __init__(self, verbose=False):
        """初始化查詢器"""
        self.mg = mygene.MyGeneInfo()
        self.verbose = verbose
        self.default_fields = 'ensembl.gene,symbol,entrezgene,name,uniprot,refseq'

    def query_by_symbol(self, symbol: str = 'SQSTM1') -> Optional[Dict]:
        """通過基因符號查詢"""
        if self.verbose:
            print(f"[查詢] 使用符號: {symbol}")

        results = self.mg.querymany(
            [symbol],
            scopes='symbol',
            species='human',
            fields=self.default_fields,
            verbose=self.verbose
        )

        if results and len(results) > 0:
            return results[0]
        return None

    def query_by_ensembl(self, ensembl_id: str = 'ENSG00000161011') -> Optional[Dict]:
        """通過 Ensembl ID 查詢"""
        if self.verbose:
            print(f"[查詢] 使用 Ensembl ID: {ensembl_id}")

        try:
            return self.mg.getgene(
                ensembl_id,
                fields=self.default_fields
            )
        except Exception as e:
            if self.verbose:
                print(f"[錯誤] {str(e)}")
            return None

    def query_by_entrez(self, entrez_id: int = 8878) -> Optional[Dict]:
        """通過 Entrez Gene ID 查詢"""
        if self.verbose:
            print(f"[查詢] 使用 Entrez ID: {entrez_id}")

        try:
            return self.mg.getgene(
                entrez_id,
                fields=self.default_fields
            )
        except Exception as e:
            if self.verbose:
                print(f"[錯誤] {str(e)}")
            return None

    def test_aliases(self, aliases: Optional[List[str]] = None) -> Dict[str, bool]:
        """測試別名是否可查詢"""
        if aliases is None:
            aliases = SQSTM1_INFO['aliases']

        if self.verbose:
            print(f"\n[測試] 測試 {len(aliases)} 個別名...")

        results = {}
        for alias in aliases:
            try:
                query_result = self.mg.query(
                    f'symbol:{alias}',
                    species='human',
                    size=1
                )
                results[alias] = query_result['total'] > 0
                if self.verbose and results[alias]:
                    print(f"  ✓ {alias:10} -> 找到")
                elif self.verbose:
                    print(f"  ✗ {alias:10} -> 未找到")
            except Exception as e:
                results[alias] = False
                if self.verbose:
                    print(f"  ✗ {alias:10} -> 錯誤: {str(e)}")

        return results

    def get_mapping_summary(self, data: Optional[Dict] = None) -> Dict:
        """獲取映射摘要信息"""
        if data is None:
            data = self.query_by_symbol()

        if not data:
            return {}

        ensembl_info = data.get('ensembl', {})
        if isinstance(ensembl_info, dict):
            ensembl_id = ensembl_info.get('gene')
        else:
            ensembl_id = None

        return {
            'symbol': data.get('symbol'),
            'gene_name': data.get('name'),
            'entrez_id': data.get('entrezgene'),
            'ensembl_id': ensembl_id,
            'uniprot_id': data.get('uniprot'),
            'refseq': data.get('refseq')
        }

    def batch_query(self, genes: List[str]) -> Dict:
        """批量查詢多個基因"""
        if self.verbose:
            print(f"\n[批量查詢] 查詢 {len(genes)} 個基因...")

        results = self.mg.querymany(
            genes,
            scopes='symbol',
            species='human',
            fields=self.default_fields,
            verbose=self.verbose
        )

        return {r.get('symbol', r.get('_id')): r for r in results}

    def print_full_info(self, symbol: str = 'SQSTM1'):
        """打印完整的基因信息"""
        print(f"\n{'='*70}")
        print(f"SQSTM1 基因完整信息查詢")
        print(f"{'='*70}\n")

        # 查詢基本信息
        data = self.query_by_symbol(symbol)
        if data:
            mapping = self.get_mapping_summary(data)
            print("基本信息:")
            print(f"  官方符號: {mapping['symbol']}")
            print(f"  基因名稱: {mapping['gene_name']}")
            print(f"  Entrez ID: {mapping['entrez_id']}")
            print(f"  Ensembl ID: {mapping['ensembl_id']}")
            print(f"  UniProt ID: {mapping['uniprot_id']}")

            if mapping['refseq']:
                print(f"  RefSeq: {mapping['refseq']}")

            # 打印原始 JSON(用於調試)
            print("\n原始數據(JSON):")
            print(json.dumps(data, indent=2, default=str))
        else:
            print(f"[錯誤] 無法找到 {symbol} 的基因信息")

        # 測試別名
        print("\n" + "="*70)
        print("別名測試結果:")
        print("="*70)
        alias_results = self.test_aliases()
        found_count = sum(1 for v in alias_results.values() if v)
        print(f"\n找到 {found_count}/{len(alias_results)} 個別名:")
        for alias, found in sorted(alias_results.items()):
            status = "✓ 可用" if found else "✗ 不可用"
            print(f"  {alias:10} -> {status}")


def main():
    """主函數"""
    print("SQSTM1 基因查詢工具")
    print("-" * 70)

    # 建立查詢器實例
    querier = SQSTM1Querier(verbose=True)

    # 方法 1: 使用官方符號查詢
    print("\n[方法 1] 使用官方符號查詢")
    print("-" * 70)
    result = querier.query_by_symbol('SQSTM1')
    if result:
        mapping = querier.get_mapping_summary(result)
        print("\n✓ 查詢成功!")
        print(f"  符號: {mapping['symbol']}")
        print(f"  Ensembl ID: {mapping['ensembl_id']}")
        print(f"  Entrez ID: {mapping['entrez_id']}")
    else:
        print("\n✗ 查詢失敗")

    # 方法 2: 使用 Ensembl ID 查詢
    print("\n\n[方法 2] 使用 Ensembl ID 查詢")
    print("-" * 70)
    result = querier.query_by_ensembl('ENSG00000161011')
    if result:
        mapping = querier.get_mapping_summary(result)
        print("\n✓ 查詢成功!")
        print(f"  符號: {mapping['symbol']}")
        print(f"  Ensembl ID: {mapping['ensembl_id']}")
        print(f"  Entrez ID: {mapping['entrez_id']}")
    else:
        print("\n✗ 查詢失敗")

    # 方法 3: 使用 Entrez ID 查詢
    print("\n\n[方法 3] 使用 Entrez ID 查詢")
    print("-" * 70)
    result = querier.query_by_entrez(8878)
    if result:
        mapping = querier.get_mapping_summary(result)
        print("\n✓ 查詢成功!")
        print(f"  符號: {mapping['symbol']}")
        print(f"  Ensembl ID: {mapping['ensembl_id']}")
        print(f"  Entrez ID: {mapping['entrez_id']}")
    else:
        print("\n✗ 查詢失敗")

    # 方法 4: 測試別名
    print("\n\n[方法 4] 測試別名")
    print("-" * 70)
    alias_results = querier.test_aliases()
    found = {k: v for k, v in alias_results.items() if v}
    not_found = {k: v for k, v in alias_results.items() if not v}

    print(f"\n✓ 可用別名 ({len(found)}/{len(alias_results)}):")
    for alias in sorted(found.keys()):
        print(f"  • {alias}")

    if not_found:
        print(f"\n✗ 不可用別名 ({len(not_found)}/{len(alias_results)}):")
        for alias in sorted(not_found.keys()):
            print(f"  • {alias}")

    # 方法 5: 批量查詢
    print("\n\n[方法 5] 批量查詢多個基因")
    print("-" * 70)
    genes_to_query = ['SQSTM1', 'p62', 'CDK2', 'TP53']
    batch_results = querier.batch_query(genes_to_query)
    print(f"\n查詢結果 ({len(batch_results)}/{len(genes_to_query)} 成功):")
    for gene, data in batch_results.items():
        ensembl = data.get('ensembl', {})
        ensembl_id = ensembl.get('gene') if isinstance(ensembl, dict) else 'N/A'
        print(f"  • {gene:10} -> Ensembl: {ensembl_id}")

    # 完整信息
    print("\n\n[完整信息]")
    print("-" * 70)
    querier.print_full_info()

    print("\n" + "="*70)
    print("查詢完成")
    print("="*70)


if __name__ == '__main__':
    main()
