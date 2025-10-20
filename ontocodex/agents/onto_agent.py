from typing import Dict, Any
from ..retrieval.priority_retriever import PriorityRetriever
from ..chains.evidence import EvidenceEnforcer
from ..mapping.tools import MappingTool, MappingArgs
from ..core.memory import ConversationMemory
from .planner_llm import TinyPlanner

class OntoCodexAgent:
    """Agent with memory and a tiny LLM planner."""
    def __init__(self, retriever: PriorityRetriever, enforcer: EvidenceEnforcer,
                 mapper: MappingTool, memory: ConversationMemory, planner: TinyPlanner | None = None,
                 data_dir: str = "data"):
        self.retriever = retriever
        self.enforcer = enforcer
        self.mapper = mapper
        self.memory = memory
        self.data_dir = data_dir
        self.planner = planner or TinyPlanner(memory)

    def invoke(self, user_text: str) -> Dict[str, Any]:
        # 1) Record user turn
        self.memory.add("user", user_text)

        # 2) Planner decides action
        plan = self.planner.plan(user_text)

        # 3) Execute
        if plan["action"] == "MAP":
            # infer term from last user text if not provided
            term = user_text
            table = plan["table"] or self.memory.get_slot("last_table", "rxnorm")
            res = self.mapper.invoke(MappingArgs(term=term, table=table, data_dir=self.data_dir))
            out = {"plan": plan, "result": res}
        else:  # PHENOTYPE
            concept = self.retriever.invoke(user_text)
            ev = []
            if concept.get("definition"):
                ev.append({"text": concept["definition"], "source": concept.get("source",""), "path": "definition"})
            concept["evidence"] = ev
            concept = self.enforcer.invoke(concept)
            out = {"plan": plan, "result": concept}

        # 4) Write agent turn + update slots
        self.memory.add("agent", out)
        if plan.get("table"):
            self.memory.set_slot("last_table", plan["table"])
        return out
