
from typing import Dict, Any, List, Optional
import os
from datetime import datetime, timezone
from ..mapping.tools import MappingTool, MappingArgs
from ..core.memory import ConversationMemory

def _now_iso():
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00","Z")

class TerminologyAgent:
    """
    Maps entities to RxNorm/SNOMED/LOINC with provenance + confidence.
    Confidence heuristic:
      - start from mapping tool's top score (0..100)
      - normalize: score/100
      - adjust by table priority (rxnorm=1.0, snomed=0.95, loinc=0.9)
    Provenance includes: mapping file path, table name, timestamp.
    """
    def __init__(self, data_dir: str, memory: ConversationMemory):
        self.memory = memory
        self.data_dir = data_dir
        self.tool = MappingTool()

    @staticmethod
    def _table_priority(table: str) -> float:
        t = (table or "").lower()
        if t == "rxnorm": return 1.0
        if t == "snomed": return 0.95
        if t == "loinc":  return 0.90
        return 0.85

    def map_terms(self, terms: List[str]) -> Dict[str, Any]:
        out: List[Dict[str, Any]] = []
        for term in terms:
            for table in ["rxnorm", "snomed", "loinc"]:
                args = MappingArgs(term=term, table=table, data_dir=self.data_dir, limit=5)
                res = self.tool.invoke(args)
                if not isinstance(res, dict) or not res.get("ranked"):
                    continue
                top = res.get("top") or {}
                try:
                    score = float(top.get("score_str", 0.0))
                except Exception:
                    score = float(top.get("score", 0.0))
                conf = min(max(score / 100.0, 0.0), 1.0) * self._table_priority(table)
                file_map = {"rxnorm":"rxnorm_omop.csv","snomed":"snomed_omop.csv","loinc":"loinc_omop.csv"}
                src_file = os.path.join(self.data_dir, file_map.get(table, f"{table}.csv"))
                prov = {"source":"OMOP","mapping_table":table.upper(),"mapping_file":src_file if os.path.exists(src_file) else None,"timestamp":_now_iso()}
                out.append({"term":term,"table":table,"top":top,"ranked":res.get("ranked"),"confidence":round(conf,3),"provenance":prov})
        by_term = {}
        for item in out:
            by_term.setdefault(item["term"], []).append(item)
        return {"mappings": out, "by_term": by_term}
