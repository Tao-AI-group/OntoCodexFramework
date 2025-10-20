
from typing import Dict, Any, Optional, List
from ..core.memory import ConversationMemory
import json

try:
    from .planner_llm import TinyPlanner
except Exception:
    TinyPlanner = None

SYSTEM_GUIDE = (
    "You are the LLM Planner for OntoCodex. "
    "Decompose the user's enrichment goal into targets, relations, and entities. "
    "Return JSON ONLY with keys: targets, relations, entities, notes."
)

class LLMAgent:
    def __init__(self, memory: ConversationMemory, backend: Optional[str] = None):
        self.memory = memory
        self.backend = backend
        self.planner = TinyPlanner(memory) if TinyPlanner else None

    def plan(self, user_goal: str, disease_or_class: Optional[str] = None) -> Dict[str, Any]:
        prompt = (
            f"Goal: {user_goal}\n"
            f"Target: {disease_or_class or 'N/A'}\n"
            f"History:\n{self.memory.to_prompt(8)}\n"
            "Return JSON only."
        )
        if self.planner:
            raw = self.planner.llm.invoke([
                {"role":"system","content": SYSTEM_GUIDE},
                {"role":"user","content": prompt}
            ]).get("content", "{}")
        else:
            raw = "{}"
        try:
            plan = json.loads(raw)
        except Exception:
            plan = {"targets":[disease_or_class or user_goal],"relations":["treated_with","has_symptom","has_lab_test"],"entities":[],"notes":"fallback"}
        return plan

    @staticmethod
    def harmonize_confidence(relations: List[Dict[str,Any]], mappings: Dict[str, Any]) -> List[Dict[str,Any]]:
        best_map_conf = {}
        for m in mappings.get("mappings", []):
            term = str(m.get("term","")).lower()
            conf = float(m.get("confidence", 0.0))
            if term and conf > best_map_conf.get(term, 0.0):
                best_map_conf[term] = conf
        out = []
        for r in relations:
            obj_label = str(r.get("object","")).lower()
            r_conf = float(r.get("confidence", 0.0))
            m_conf = best_map_conf.get(obj_label, 0.0)
            final_conf = 0.6 * r_conf + 0.4 * m_conf
            rr = dict(r)
            rr["final_confidence"] = round(final_conf, 3)
            out.append(rr)
        return out
