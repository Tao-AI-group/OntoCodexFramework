from typing import Dict, Any
from ..retrieval.priority_retriever import PriorityRetriever
from ..chains.evidence import EvidenceEnforcer
from ..mapping.tools import MappingTool, MappingArgs

class OntoCodexAgent:
    """LangChain-like agent that routes to OntoCodex tools."""
    def __init__(self, retriever: PriorityRetriever, enforcer: EvidenceEnforcer, mapper: MappingTool):
        self.retriever = retriever
        self.enforcer = enforcer
        self.mapper = mapper

    def invoke(self, task: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        t = task.lower()
        if "phenotype" in t or "disease" in t:
            concept = self.retriever.invoke(payload["term"])
            ev = []
            if concept.get("definition"):
                ev.append({"text": concept["definition"], "source": concept.get("source",""), "path": "definition"})
            concept["evidence"] = ev
            concept = self.enforcer.invoke(concept)
            return {"task": "phenotype", "result": concept}
        if "map" in t or "code" in t:
            args = MappingArgs(**payload)
            mapped = self.mapper.invoke(args)
            return {"task": "mapping", "result": mapped}
        if "guideline" in t:
            return {"task": "guidelines", "result": {"note":"no guideline tool wired"}}
        return {"error": f"Unrecognized task '{task}'"}
