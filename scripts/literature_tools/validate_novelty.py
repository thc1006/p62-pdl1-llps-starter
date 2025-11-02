#!/usr/bin/env python3
"""
Validate Novelty of Findings via PubMed Literature Search
==========================================================
Check if our "novel" correlations have been reported before
"""
import requests
import time
from pathlib import Path
import json

def search_pubmed(query, retmax=100):
    """Search PubMed E-utilities API"""
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"

    # Search
    search_url = f"{base_url}esearch.fcgi"
    params = {
        "db": "pubmed",
        "term": query,
        "retmax": retmax,
        "retmode": "json",
        "mindate": "2020/01/01",
        "maxdate": "2025/11/02",
        "datetype": "pdat"
    }

    try:
        response = requests.get(search_url, params=params, timeout=30)
        response.raise_for_status()
        data = response.json()

        count = int(data['esearchresult']['count'])
        pmids = data['esearchresult']['idlist']

        print(f"  Query: {query}")
        print(f"  Results (2020-2025): {count} papers")

        return count, pmids

    except Exception as e:
        print(f"  Error: {e}")
        return 0, []

def validate_correlations():
    """Validate each correlation's novelty"""
    print("="*80)
    print("NOVELTY VALIDATION VIA PUBMED (2020-2025)")
    print("="*80)

    correlations = {
        "1. CMTM6-STUB1 negative correlation": [
            "CMTM6 AND STUB1",
            "CMTM6 AND CHIP ubiquitin ligase",
            "CMTM6 AND STUB1 correlation",
            "CMTM6 AND STUB1 lung cancer"
        ],
        "2. CD274-CMTM6 positive correlation": [
            "PD-L1 AND CMTM6 correlation",
            "CD274 AND CMTM6 lung cancer",
            "PD-L1 AND CMTM6 expression correlation"
        ],
        "3. CD274-STUB1 negative correlation": [
            "PD-L1 AND STUB1",
            "CD274 AND CHIP ubiquitin ligase",
            "PD-L1 AND STUB1 ubiquitination",
            "PD-L1 degradation STUB1"
        ],
        "4. CD274-HIP1R negative correlation": [
            "PD-L1 AND HIP1R",
            "CD274 AND HIP1R endocytosis",
            "PD-L1 AND HIP1R correlation"
        ],
        "5. SQSTM1-STUB1 positive correlation": [
            "p62 AND STUB1",
            "SQSTM1 AND CHIP ubiquitin ligase",
            "p62 AND CHIP interaction"
        ],
        "6. CMTM6-SQSTM1 negative correlation": [
            "CMTM6 AND p62",
            "CMTM6 AND SQSTM1",
            "CMTM6 AND autophagy"
        ]
    }

    results = {}

    for finding, queries in correlations.items():
        print(f"\n{finding}")
        print("-" * 60)

        total_hits = 0
        all_pmids = []

        for query in queries:
            count, pmids = search_pubmed(query, retmax=50)
            total_hits += count
            all_pmids.extend(pmids)
            time.sleep(0.4)  # NCBI rate limit

        # Deduplicate PMIDs
        unique_pmids = list(set(all_pmids))

        results[finding] = {
            "total_hits_all_queries": total_hits,
            "unique_papers": len(unique_pmids),
            "queries_searched": len(queries),
            "novelty_assessment": "HIGH" if len(unique_pmids) < 5 else "MODERATE" if len(unique_pmids) < 20 else "LOW"
        }

        print(f"  TOTAL papers found: {len(unique_pmids)} unique")
        print(f"  NOVELTY: {results[finding]['novelty_assessment']}")

    # Summary
    print("\n" + "="*80)
    print("NOVELTY ASSESSMENT SUMMARY")
    print("="*80)

    for finding, data in results.items():
        status = data['novelty_assessment']
        symbol = "[HIGH]" if status == "HIGH" else "[MOD]" if status == "MODERATE" else "[LOW]"
        print(f"\n{finding}")
        print(f"  Papers: {data['unique_papers']}")
        print(f"  Novelty: {status} {symbol}")

    # Save results
    output_dir = Path("outputs/novelty_validation")
    output_dir.mkdir(parents=True, exist_ok=True)

    results_file = output_dir / "novelty_assessment.json"
    with open(results_file, 'w') as f:
        json.dump(results, f, indent=2)

    print(f"\n[SAVED] {results_file}")

    # Generate report
    report_file = output_dir / "novelty_report.md"
    with open(report_file, 'w') as f:
        f.write("# Novelty Validation Report\n\n")
        f.write(f"**Date:** 2025-11-02\n")
        f.write(f"**Database:** PubMed (2020-2025)\n\n")

        f.write("## Summary\n\n")
        f.write("| Finding | Unique Papers | Novelty |\n")
        f.write("|---------|---------------|----------|\n")

        for finding, data in results.items():
            f.write(f"| {finding} | {data['unique_papers']} | {data['novelty_assessment']} |\n")

        f.write("\n## Interpretation\n\n")
        f.write("- **HIGH novelty (0-4 papers):** Likely first report or very understudied\n")
        f.write("- **MODERATE novelty (5-19 papers):** Some prior work, but still novel angle\n")
        f.write("- **LOW novelty (20+ papers):** Well-studied, incremental contribution\n\n")

        f.write("## Conclusion\n\n")
        high_novelty = [f for f, d in results.items() if d['novelty_assessment'] == 'HIGH']

        if len(high_novelty) >= 3:
            f.write(f"**{len(high_novelty)}/6 findings have HIGH novelty** - Strong case for Nature Communications!\n\n")
        elif len(high_novelty) >= 1:
            f.write(f"**{len(high_novelty)}/6 findings have HIGH novelty** - Good case for high-impact journal.\n\n")
        else:
            f.write("Most findings have prior literature. Consider reframing as validation/extension study.\n\n")

    print(f"[SAVED] {report_file}")

    return results

if __name__ == "__main__":
    results = validate_correlations()
