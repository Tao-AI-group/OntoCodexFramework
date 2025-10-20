from .blackboard import Blackboard
from ..agents.planner_llm import TinyPlanner
from ..core.memory import ConversationMemory

GUIDE_TERMS = ["guideline", "recommendation", "standard of care", "soc", "ada", "acc", "aha", "nih", "cdc"]

class PlannerRouter:
    def __init__(self, memory: ConversationMemory):
        self.memory = memory
        self.planner = TinyPlanner(memory)

    def route(self, bb: Blackboard, user_text: str):
        if any(t in user_text.lower() for t in GUIDE_TERMS):
            bb.post(sender="user", receiver="guideline_tool", type="task",
                    content={"task":"guidelines","term":user_text})
            return {"action":"GUIDELINE","table":None,"backend":"router-rule","raw":"ROUTE: guidelines"}
        plan = self.planner.plan(user_text)
        action = plan.get("action","PHENOTYPE").upper()
        table = (plan.get("table") or "rxnorm").lower()
        if action == "MAP":
            bb.post(sender="user", receiver="mapper", type="task",
                    content={"task":"map","term":user_text,"table":table,"limit":10})
        else:
            bb.post(sender="user", receiver="retriever", type="task",
                    content={"task":"phenotype","term":user_text})
        return plan
