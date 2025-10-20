from .base_agent import BaseAgent
from ..blackboard import Blackboard

class GuidelineAgent(BaseAgent):
    """Stub: attaches guideline references (ADA/ACC/AHA/NIH/CDC)."""
    def __init__(self, name: str = "guidelines"):
        super().__init__(name)

    def step(self, bb: Blackboard) -> None:
        for msg in bb.query(receiver=self.name, type="task"):
            if msg.content.get("task") != "guidelines":
                continue
            disease = msg.content.get("term")
            notes = [
                {"source":"ADA","note":"SOC check (stub)"},
                {"source":"ACC/AHA","note":"cardio SOC (stub)"},
                {"source":"NIH/CDC","note":"labs/policy SOC (stub)"},
            ]
            bb.post(sender=self.name, receiver="coordinator", type="result", content={
                "task":"guidelines",
                "term": disease,
                "guidelines": notes
            })
