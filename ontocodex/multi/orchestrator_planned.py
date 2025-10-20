from typing import List, Dict, Any, Optional
from .blackboard import Blackboard
from .agents.base_agent import BaseAgent
from .router_planner import PlannerRouter
from ..core.memory import ConversationMemory

class CodexOrchestratorPlanned:
    """Multi-agent orchestrator driven by LLM planner routing."""
    def __init__(self, agents: List[BaseAgent], memory: Optional[ConversationMemory] = None):
        self.agents = agents
        self.bb = Blackboard()
        self.memory = memory or ConversationMemory(max_turns=50)
        self.router = PlannerRouter(self.memory)

    def chat_turn(self, user_text: str, max_rounds: int = 4) -> Dict[str, Any]:
        # Log user turn
        self.memory.add("user", user_text)
        # Planner decides where to route
        plan = self.router.route(self.bb, user_text)
        # Run agents for a few cycles
        for _ in range(max_rounds):
            for agent in self.agents:
                agent.step(self.bb)
        # Collect results
        results = [m.content for m in self.bb.query(receiver="coordinator", type="result")]
        # Record agent output to memory
        self.memory.add("agent", {"plan": plan, "results": results})
        return {"plan": plan, "results": results}
