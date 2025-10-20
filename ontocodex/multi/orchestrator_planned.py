from typing import List, Dict, Any, Optional
from .blackboard import Blackboard
from .agents.base_agent import BaseAgent
from .router_planner import PlannerRouter
from ..core.memory import ConversationMemory
class CodexOrchestratorPlanned:
    def __init__(self, agents: List[BaseAgent], memory: Optional[ConversationMemory]=None):
        self.agents=agents; self.bb=Blackboard(); self.memory=memory or ConversationMemory(50); self.router=PlannerRouter(self.memory)
    def chat_turn(self, user_text: str, max_rounds: int = 4) -> Dict[str, Any]:
        self.memory.add('user', user_text); plan=self.router.route(self.bb, user_text)
        for _ in range(max_rounds):
            for a in self.agents: a.step(self.bb)
        results=[m.content for m in self.bb.query(receiver='coordinator', type='result')]
        self.memory.add('agent', {'plan':plan,'results':results}); return {'plan':plan,'results':results}
