from typing import Dict, Any
from .base_agent import BaseAgent
from ..blackboard import Blackboard
from ...kb.priority import KBConfig
from ...retrieval.priority_retriever import PriorityRetriever

class RetrieverAgent(BaseAgent):
    """Resolves diseases/phenotypes by strict ontology priority (DOID→MedlinePlus→HP)."""
    def __init__(self, cfg: KBConfig, name: str = "retriever"):
        super().__init__(name)
        self.retriever = PriorityRetriever(cfg)

    def step(self, bb: Blackboard) -> None:
        # Look for tasks addressed to me
        for msg in bb.query(receiver=self.name, type="task"):
            task = msg.content.get("task")
            if task != "phenotype":
                continue
            term = msg.content.get("term")
            if not term:
                continue
            concept = self.retriever.invoke(term)
            # Minimal evidence attach here; validator may enforce later
            if concept.get("definition"):
                concept["evidence"] = [{
                    "text": concept["definition"],
                    "source": concept.get("source",""),
                    "path": "definition"
                }]
            bb.post(sender=self.name, receiver="coordinator", type="result", content={
                "task": "phenotype",
                "term": term,
                "concept": concept
            })
