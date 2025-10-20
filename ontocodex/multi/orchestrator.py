from typing import List, Dict, Any
from .blackboard import Blackboard
from .agents.base_agent import BaseAgent

class CodexOrchestrator:
    """Simple coordination loop over a set of agents using a blackboard."""
    def __init__(self, agents: List[BaseAgent]):
        self.agents = agents
        self.bb = Blackboard()

    def submit(self, user_text: str) -> Dict[str, Any]:
        """Naive routing: if text mentions lab/loinc→map loinc; drug/rxnorm→map rxnorm; else phenotype.
        In a full system, you'd call your LLM planner here and post tasks to agents.
        """
        t = user_text.lower()
        if any(k in t for k in ["lab","loinc","test","assay"]):
            self.bb.post(sender="user", receiver="mapper", type="task",
                         content={"task":"map","term":user_text,"table":"loinc","limit":10})
        elif any(k in t for k in ["drug","rxnorm","med","treatment"]):
            self.bb.post(sender="user", receiver="mapper", type="task",
                         content={"task":"map","term":user_text,"table":"rxnorm","limit":10})
        elif any(k in t for k in ["guideline","standard of care","ada","acc","aha","nih","cdc"]):
            self.bb.post(sender="user", receiver="guidelines", type="task",
                         content={"task":"guidelines","term":user_text})
        else:
            self.bb.post(sender="user", receiver="retriever", type="task",
                         content={"task":"phenotype","term":user_text})
        return {"status":"submitted"}

    def run(self, max_rounds: int = 4) -> Dict[str, Any]:
        """Run a few coordination rounds. Agents can read/write the blackboard."""
        for _ in range(max_rounds):
            for agent in self.agents:
                agent.step(self.bb)

        # Collate results
        results = [m.content for m in self.bb.query(receiver="coordinator", type="result")]
        return {
            "results": results,
            "kv": dict(self.bb.kv),
            "messages": [m.__dict__ for m in self.bb.messages]
        }
