#!/usr/bin/env python3
"""
Query PubMed via E-utilities and build an evidence table (+BibTeX).

Refs:
- E-utilities overview: https://www.ncbi.nlm.nih.gov/books/NBK25499/
- Command-line Entrez Direct: https://www.ncbi.nlm.nih.gov/books/NBK179288/
"""
import argparse, os, sys, time, csv, json, re
from urllib.parse import urlencode
import requests
from lxml import etree

TOOL="p62pdl1.llps"
EMAIL=os.environ.get("CONTACT_EMAIL","you@example.com")
API_KEY=os.environ.get("Entrez_API_KEY") or os.environ.get("ENTREZ_API_KEY")

def eutils(path, params):
    base = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
    q = params.copy()
    q["tool"] = TOOL
    q["email"] = EMAIL
    if API_KEY: q["api_key"] = API_KEY
    url = base + path + "?" + urlencode(q)
    r = requests.get(url, timeout=60)
    r.raise_for_status()
    return r.text

def search(query, mindate, maxdate, retmax=200):
    txt = eutils("esearch.fcgi", {
        "db":"pubmed","term":query,
        "retmode":"json","retmax":str(retmax),
        "mindate":str(mindate),"maxdate":str(maxdate),
        "usehistory":"y"
    })
    js = json.loads(txt)
    webenv = js["esearchresult"]["webenv"]
    query_key = js["esearchresult"]["querykey"]
    count = int(js["esearchresult"]["count"])
    ids = js["esearchresult"]["idlist"]
    return ids, count, webenv, query_key

def fetch_summary(ids):
    if not ids: return []
    txt = eutils("esummary.fcgi", {
        "db":"pubmed","id":",".join(ids),"retmode":"json"
    })
    return json.loads(txt)["result"]

def fetch_xml(ids):
    if not ids: return None
    xml = eutils("efetch.fcgi", {
        "db":"pubmed","id":",".join(ids),"retmode":"xml"
    })
    return xml

def parse_records(summary_result, xml_text):
    recs = []
    pmid_set = set()
    doi_by_pmid = {}
    if xml_text:
        root = etree.fromstring(xml_text.encode("utf-8"))
        for art in root.findall(".//PubmedArticle"):
            pmid = art.findtext(".//MedlineCitation/PMID")
            dois = art.findall(".//ArticleIdList/ArticleId[@IdType='doi']")
            if pmid and dois:
                doi_by_pmid[pmid] = dois[0].text
    for k,v in summary_result.items():
        if k in ("uids","result"): continue
        pmid = v.get("uid")
        if not pmid or pmid in pmid_set: continue
        pmid_set.add(pmid)
        title = v.get("title","" ).strip()
        journal = (v.get("fulljournalname") or v.get("source") or "").strip()
        year = None
        try:
            year = int((v.get("pubdate") or "").split(" ")[0].split("-")[0])
        except Exception:
            pass
        doi = doi_by_pmid.get(pmid)
        text = (title + " " + " ".join(v.get("authors",[]).__str__()) + " " + (v.get("sortfirstauthor") or "")).lower()
        llps_methods, rigor_flags = [], []
        for kw in ["frap","fluorescence recovery","hexanediol","1,6-hexanediol","condensate","phase separation","llps"]:
            if kw in text:
                llps_methods.append(kw)
        if "hexanediol" in text or "1,6-hexanediol" in text:
            rigor_flags.append("hexanediol-caveat")
        recs.append({
            "PMID": pmid,
            "DOI": doi or "",
            "Year": year or "",
            "Journal": journal,
            "Title": title,
            "System": "",
            "Assay": "",
            "Manipulation": "",
            "Key_Proteins": "",
            "Finding": "",
            "Strength": "",
            "LLPS_methods": ";".join(sorted(set(llps_methods))),
            "Rigor_flags": ";".join(sorted(set(rigor_flags))),
        })
    return recs

def to_bib(recs):
    lines = []
    for r in recs:
        key = f"PMID{r['PMID']}"
        title = r["Title"].replace("{"," ").replace("}"," ")
        year = r["Year"] or ""
        journal = (r["Journal"] or "").replace("{"," ").replace("}"," ")
        doi = r["DOI"]
        lines.append("@article{%s,\n  title={%s},\n  journal={%s},\n  year={%s},\n  doi={%s},\n  pmid={%s}\n}\n" %
                     (key, title, journal, year, doi, r["PMID"]))
    return "".join(lines)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--query", required=True)
    ap.add_argument("--mindate", type=int, default=2017)
    ap.add_argument("--maxdate", type=int, default=3000)
    ap.add_argument("--retmax", type=int, default=200)
    ap.add_argument("--out", default="outputs/evidence")
    args = ap.parse_args()
    os.makedirs(args.out, exist_ok=True)

    ids, count, webenv, qk = search(args.query, args.mindate, args.maxdate, args.retmax)
    summ = fetch_summary(ids)
    xml = fetch_xml(ids)
    recs = parse_records(summ, xml)
    if not recs:
        # still write headers
        recs = []
    # CSV
    import csv
    headers = ["PMID","DOI","Year","Journal","Title","System","Assay","Manipulation","Key_Proteins","Finding","Strength","LLPS_methods","Rigor_flags"]
    with open(os.path.join(args.out, "evidence_table.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=headers)
        w.writeheader()
        for r in recs: w.writerow(r)
    # BibTeX
    with open(os.path.join(args.out, "bib.bib"), "w", encoding="utf-8") as f:
        f.write(to_bib(recs))
    with open(os.path.join(args.out, "summary.md"), "w", encoding="utf-8") as f:
        f.write(f"# Triage Summary\n\nTotal returned (first page): {len(recs)}\n")
    print("Wrote triage outputs to", args.out)

if __name__ == "__main__":
    main()
