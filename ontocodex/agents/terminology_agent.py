from typing import Dict, Any, List
import os
from ..mapping.tools import MappingTool, MappingArgs
from ..core.memory import ConversationMemory

class TerminologyAgent:
    def __init__(self, data_dir: str, memory: ConversationMemory):
        self.memory = memory
        self.data_dir = data_dir
        self.tool = MappingTool()

    def map_terms(self, terms: List[str]) -> Dict[str, Any]:
        out = []
        for t in terms:
            for table in ["rxnorm","snomed","loinc"]:
                res = self.tool.invoke(MappingArgs(term=t, table=table, data_dir=self.data_dir, limit=5))
                if isinstance(res, dict) and res.get("ranked"):
                    out.append({"term": t, "table": table, "top": res.get("top"), "ranked": res.get("ranked")})
        return {"mappings": out}
