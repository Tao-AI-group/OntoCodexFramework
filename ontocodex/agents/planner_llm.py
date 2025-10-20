from typing import Dict, Any
from ..core.memory import ConversationMemory
from ..io.planner_logger import PlannerLogger

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
    Logs every decision for retraining.
    """
    def __init__(self, memory: ConversationMemory, llm=None, log_dir: str = "logs"):
        self.memory = memory
        self.llm = llm or DefaultLLM()
        self.logger = PlannerLogger(log_dir)

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

        action, table = "PHENOTYPE", None
        if "MAP" in content.upper():
            action = "MAP"
            if "rxnorm" in content.lower(): table = "rxnorm"
            elif "loinc" in content.lower(): table = "loinc"
            elif "snomed" in content.lower(): table = "snomed"

        result = {"action": action, "table": table, "backend": LLM_BACKEND, "raw": content}

        # --- Log the planner output ---
        self.logger.log({
            "user_text": user_text,
            "memory_context": hist,
            "model_backend": LLM_BACKEND,
            "model_output": content,
            "parsed_action": action,
            "parsed_table": table
        })

        return result
