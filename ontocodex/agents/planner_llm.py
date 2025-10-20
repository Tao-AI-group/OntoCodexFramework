from typing import Dict, Any
from ..core.memory import ConversationMemory
from ..io.llm_stub import TinyLLM

class TinyPlanner:
    """
    LLM-driven planner that decides: PHENOTYPE vs MAP(table={rxnorm|loinc|snomed}).
    Uses conversation memory to fill missing slots (e.g., table or term).
    """
    def __init__(self, memory: ConversationMemory, llm: TinyLLM | None = None):
        self.memory = memory
        self.llm = llm or TinyLLM()

    def plan(self, user_text: str) -> Dict[str, Any]:
        hist = self.memory.to_prompt(last_n=6)
        msg = [
            {"role":"system","content":"You are a planner that outputs a single ACTION."},
            {"role":"user","content": f"History:\n{hist}\n\nUser: {user_text}"},
        ]
        out = self.llm.invoke(msg).get("content","ACTION: PHENOTYPE")
        action = "PHENOTYPE"
        table = None
        if "MAP" in out.upper():
            action = "MAP"
            if "rxnorm" in out.lower(): table = "rxnorm"
            elif "loinc" in out.lower(): table = "loinc"
            elif "snomed" in out.lower(): table = "snomed"
        return {"action": action, "table": table}
