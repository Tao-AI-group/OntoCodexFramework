from typing import Dict, Any, Optional
from ..core.memory import ConversationMemory
try:
    from .planner_llm import TinyPlanner
except Exception:
    TinyPlanner = None

SYSTEM_GUIDE = (
    "You are the Large Language Model Agent for OntoCodex. "
    "Coordinate ontology enrichment and output JSON only with keys: targets, entities, needs, notes."
)

class LLMAgent:
    def __init__(self, memory: ConversationMemory, backend: Optional[str] = None):
        self.memory = memory
        self.backend = backend
        self.planner = TinyPlanner(memory) if TinyPlanner else None

    def plan(self, user_goal: str, disease_or_class: Optional[str] = None) -> Dict[str, Any]:
        prompt = f"Goal: {user_goal}\nTarget: {disease_or_class or 'N/A'}\nHistory:\n{self.memory.to_prompt(8)}\nReturn JSON only."
        if self.planner:
            resp = self.planner.llm.invoke([{"role":"system","content":SYSTEM_GUIDE},{"role":"user","content":prompt}]).get("content","{}")
        else:
            resp = "{}"
        import json
        try:
            plan = json.loads(resp)
        except Exception:
            plan = {"targets":[disease_or_class or user_goal],"entities":[],"needs":["ontology","evidence","mappings"],"notes":"fallback"}
        return plan
