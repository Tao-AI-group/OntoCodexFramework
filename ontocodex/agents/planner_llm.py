from typing import Dict, Any
from ..core.memory import ConversationMemory

# Auto-detect LLM backend
LLM_BACKEND = None
try:
    from ..io.llm_openai import OpenAIPlannerLLM
    LLM_BACKEND = "openai"
    DefaultLLM = OpenAIPlannerLLM
except Exception:
    try:
        from ..io.llm_anthropic import AnthropicPlannerLLM
        LLM_BACKEND = "anthropic"
        DefaultLLM = AnthropicPlannerLLM
    except Exception:
        from ..io.llm_stub import TinyLLM
        LLM_BACKEND = "stub"
        DefaultLLM = TinyLLM

class TinyPlanner:
    """
    Planner powered by real LLMs (OpenAI/Anthropic) with stub fallback.
    The LLM must output one of:
      - ACTION: PHENOTYPE
      - ACTION: MAP table=<rxnorm|loinc|snomed>
    """
    def __init__(self, memory: ConversationMemory, llm=None):
        self.memory = memory
        self.llm = llm or DefaultLLM()

    def plan(self, user_text: str) -> Dict[str, Any]:
        hist = self.memory.to_prompt(last_n=6)
        messages = [
            {"role": "system", "content": (
                "You are an expert planner for an ontology agent (OntoCodex). "
                "Decide the correct action based on user intent and past turns.\n"
                "Return exactly one line in the format:\n"
                "ACTION: PHENOTYPE or ACTION: MAP table=<rxnorm|loinc|snomed>."
            )},
            {"role": "user", "content": f"History:\n{hist}\n\nUser: {user_text}"}
        ]
        try:
            content = self.llm.invoke(messages).get("content", "ACTION: PHENOTYPE")
        except Exception as e:
            content = f"ACTION: PHENOTYPE  # fallback ({e})"
        action = "PHENOTYPE"
        table = None
        if "MAP" in content.upper():
            action = "MAP"
            if "rxnorm" in content.lower(): table = "rxnorm"
            elif "loinc" in content.lower(): table = "loinc"
            elif "snomed" in content.lower(): table = "snomed"
        return {"action": action, "table": table, "backend": LLM_BACKEND, "raw": content}
