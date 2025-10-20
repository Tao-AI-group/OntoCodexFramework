"""
Guideline retrievers for PubMed (≤5 years) and institutional sources (ADA/ACC/AHA/NIH/CDC).
Designed to be lightweight (urllib only). Real endpoints can be enabled later.
"""
from typing import List, Dict, Optional
from datetime import datetime, timedelta
import json, urllib.parse, urllib.request

ESEARCH = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
ESUMMARY = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"

def _http_json(url: str, params: Dict[str, str]) -> Dict:
    q = urllib.parse.urlencode(params)
    with urllib.request.urlopen(url + "?" + q) as resp:
        data = resp.read().decode("utf-8")
    return json.loads(data)

def pubmed_guidelines(term: str, max_results: int = 5) -> List[Dict]:
    today = datetime.utcnow()
    five_years_ago = today - timedelta(days=5*365)
    query = f'("{term}"[Title/Abstract]) AND (guideline[Title] OR recommendation[Title])'
    params = {
        "db": "pubmed",
        "retmax": str(max_results),
        "term": query,
        "retmode": "json",
        "mindate": str(five_years_ago.year),
        "maxdate": str(today.year),
    }
    try:
        es = _http_json(ESEARCH, params)
        ids = es.get("esearchresult", {}).get("idlist", [])
        if not ids:
            return []
        summ = _http_json(ESUMMARY, {"db":"pubmed","id":",".join(ids),"retmode":"json"})
        out = []
        for pmid in ids:
            rec = summ.get("result", {}).get(pmid)
            if not rec:
                continue
            pubdate = rec.get("pubdate","")
            year = int(pubdate[:4]) if pubdate[:4].isdigit() else None
            if year and year < five_years_ago.year:
                continue
            out.append({
                "source": "PubMed",
                "title": rec.get("title"),
                "url": f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/",
                "year": year,
                "pmid": pmid
            })
        return out
    except Exception:
        return []

def _inst_stub(source: str, term: str) -> List[Dict]:
    year = datetime.utcnow().year
    return [{
        "source": source,
        "title": f"{source} guideline for {term} ({year})",
        "url": f"https://example.org/{source.lower()}/{term}",
        "year": year
    }]

def ada_guidelines(term: str) -> List[Dict]:
    return _inst_stub("ADA", term)

def acc_guidelines(term: str) -> List[Dict]:
    return _inst_stub("ACC", term)

def aha_guidelines(term: str) -> List[Dict]:
    return _inst_stub("AHA", term)

def nih_guidelines(term: str) -> List[Dict]:
    return _inst_stub("NIH", term)

def cdc_guidelines(term: str) -> List[Dict]:
    return _inst_stub("CDC", term)
