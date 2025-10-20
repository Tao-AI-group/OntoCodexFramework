from typing import Dict, Any
import os
from ..core.memory import ConversationMemory

# 1) Prefer local fine-tuned planner if provided
LLM_BACKEND = None
LOCAL_PATH = os.environ.get("ONTOCODEX_PLANNER_LOCAL_PATH")
if LOCAL_PATH:
    try:
        from ..io.planner_local import LocalPlannerModel as DefaultLLM
        LLM_BACKEND = "local-ft"
    except Exception:
        LOCAL_PATH = None

# 2) Else try OpenAI, then Anthropic, else stub
if not LOCAL_PATH:
    try:
        from ..io.llm_openai import OpenAIPlannerLLM as DefaultLLM
        LLM_BACKEND = "openai"
    except Exception:
        try:
            from ..io.llm_anthropic import AnthropicPlannerLLM as DefaultLLM
            LLM_BACKEND = "anthropic"
        except Exception:
            from ..io.llm_stub import TinyLLM as DefaultLLM
            LLM_BACKEND = "stub"

# Optional logger (if available)
try:
    from ..io.planner_logger import PlannerLogger
except Exception:
    PlannerLogger = None

class TinyPlanner:
    """
    Planner that uses:
      - Local fine-tuned HF model if ONTOCODEX_PLANNER_LOCAL_PATH is set
      - Else OpenAI → Anthropic → Stub fallback
    Logs decisions if planner_logger is available.
    """
    def __init__(self, memory: ConversationMemory, llm=None, log_dir: str = "logs"):
        self.memory = memory
        self.llm = llm or (DefaultLLM() if LLM_BACKEND != "local-ft" else DefaultLLM(model_path=LOCAL_PATH))
        self.logger = PlannerLogger(log_dir) if PlannerLogger else None

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
        if self.logger:
            self.logger.log({
                "user_text": user_text,
                "memory_context": hist,
                "model_backend": LLM_BACKEND,
                "model_output": content,
                "parsed_action": action,
                "parsed_table": table
            })
        return result
