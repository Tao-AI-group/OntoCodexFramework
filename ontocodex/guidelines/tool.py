"""
GuidelineTool: fetches recent guideline-like entries from PubMed E-utilities.
"""
from typing import List, Dict, Any
import json
import urllib.parse
import urllib.request

PUBMED_ESEARCH = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
PUBMED_ESUMMARY = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"

class GuidelineTool:
    def __init__(self, max_results: int = 5, years_back: int = 5):
        self.max_results = max_results
        self.years_back = years_back

    def _http_json(self, url: str, params: Dict[str, Any]) -> Dict[str, Any]:
        q = urllib.parse.urlencode(params)
        with urllib.request.urlopen(url + "?" + q) as resp:
            data = resp.read().decode("utf-8")
        return json.loads(data)

    def search_pubmed(self, term: str) -> List[Dict[str, Any]]:
        qry = f'("{term}"[Title/Abstract]) AND (guideline[Title] OR recommendation[Title])'
        es = self._http_json(PUBMED_ESEARCH, {"db":"pubmed","retmax":str(self.max_results),"term":qry,"retmode":"json"})
        ids = es.get("esearchresult", {}).get("idlist", [])
        if not ids:
            return []
        summ = self._http_json(PUBMED_ESUMMARY, {"db":"pubmed","id":",".join(ids),"retmode":"json"})
        out = []
        for k, v in summ.get("result", {}).items():
            if k == "uids": continue
            title = v.get("title", "")
            pubdate = (v.get("pubdate") or "")[:4]
            out.append({"source":"PubMed","title":title,"url":f"https://pubmed.ncbi.nlm.nih.gov/{k}/","year":pubdate})
        return out

    def invoke(self, term: str) -> List[Dict[str, Any]]:
        try:
            return self.search_pubmed(term)
        except Exception as e:
            return [{"error": f"{e}"}]
