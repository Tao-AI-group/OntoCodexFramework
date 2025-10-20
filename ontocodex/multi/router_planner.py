from typing import Dict, Any
from .blackboard import Blackboard
from ..agents.planner_llm import TinyPlanner
from ..core.memory import ConversationMemory

class PlannerRouter:
    """
    Wraps the LLM TinyPlanner to decide which agent to task.
    Posts tasks to the blackboard for specific agents:
      - 'retriever' for PHENOTYPE
      - 'mapper' for MAP (table={rxnorm|loinc|snomed})
      - future: 'guidelines' for guideline actions
    """
    def __init__(self, memory: ConversationMemory):
        self.memory = memory
        self.planner = TinyPlanner(memory)

    def route(self, bb: Blackboard, user_text: str) -> Dict[str, Any]:
        plan = self.planner.plan(user_text)
        action = plan.get("action","PHENOTYPE").upper()
        table = (plan.get("table") or "").lower()

        if action == "MAP":
            bb.post(sender="user", receiver="mapper", type="task",
                    content={"task":"map","term":user_text,"table":table or "rxnorm","limit":10})
        else:  # PHENOTYPE default
            bb.post(sender="user", receiver="retriever", type="task",
                    content={"task":"phenotype","term":user_text})
        return plan
