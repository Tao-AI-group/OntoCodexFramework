from typing import Dict, Any
from .base_agent import BaseAgent
from ..blackboard import Blackboard
from ...mapping.tools import MappingTool, MappingArgs

class MapperAgent(BaseAgent):
    """Maps free text to vocabularies with re-ranking (RxNorm/LOINC/SNOMED)."""
    def __init__(self, data_dir: str, name: str = "mapper"):
        super().__init__(name)
        self.mapper = MappingTool()
        self.data_dir = data_dir

    def step(self, bb: Blackboard) -> None:
        for msg in bb.query(receiver=self.name, type="task"):
            if msg.content.get("task") != "map":
                continue
            term = msg.content.get("term")
            table = msg.content.get("table")
            limit = int(msg.content.get("limit", 5))
            if not term or not table:
                continue
            res = self.mapper.invoke(MappingArgs(term=term, table=table, limit=limit, data_dir=self.data_dir))
            bb.post(sender=self.name, receiver="coordinator", type="result", content={
                "task": "map",
                "term": term,
                "table": table,
                "result": res
            })
