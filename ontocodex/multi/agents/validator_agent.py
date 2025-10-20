from .base_agent import BaseAgent
from ..blackboard import Blackboard

class ValidatorAgent(BaseAgent):
    """Rejects results with no evidence chain; passes-through otherwise."""
    def __init__(self, name: str = "validator"):
        super().__init__(name)

    def step(self, bb: Blackboard) -> None:
        # Validate latest phenotype result (if any)
        last = bb.latest(receiver="coordinator", type="result")
        if not last:
            return
        content = last.content
        if content.get("task") == "phenotype":
            concept = content.get("concept", {})
            evidence = concept.get("evidence", [])
            status = "ACCEPTED" if evidence else "REJECTED_NO_EVIDENCE"
            concept["status"] = status
            bb.post(sender=self.name, receiver="coordinator", type="result", content={
                "task":"validation",
                "term": content.get("term"),
                "status": status
            })
