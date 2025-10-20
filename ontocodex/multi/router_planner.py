from .blackboard import Blackboard
from ..agents.planner_llm import TinyPlanner
from ..core.memory import ConversationMemory
class PlannerRouter:
    def __init__(self, memory: ConversationMemory): self.memory=memory; self.planner=TinyPlanner(memory)
    def route(self, bb: Blackboard, user_text: str):
        plan=self.planner.plan(user_text); action=plan.get('action','PHENOTYPE').upper(); table=(plan.get('table') or 'rxnorm').lower()
        if action=='MAP': bb.post(sender='user', receiver='mapper', type='task', content={'task':'map','term':user_text,'table':table,'limit':10})
        else: bb.post(sender='user', receiver='retriever', type='task', content={'task':'phenotype','term':user_text})
        return plan
