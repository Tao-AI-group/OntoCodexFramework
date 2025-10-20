from typing import Dict, Any, Optional
from .memory import ConversationMemory
from ..agents.llm_agent import LLMAgent
from ..agents.ontology_reader_agent import OntologyReaderAgent
from ..agents.knowledge_agent import KnowledgebaseAgent
from ..agents.terminology_agent import TerminologyAgent
from ..agents.enrichment_agent import EnrichmentScriptAgent

class OntoCodexOrchestrator:
    def __init__(self, data_dir: str = "data", llm_backend: Optional[str] = None):
        self.memory = ConversationMemory(max_turns=200)
        self.llm = LLMAgent(memory=self.memory, backend=llm_backend)
        self.reader = OntologyReaderAgent(data_dir=data_dir, memory=self.memory)
        self.kb = KnowledgebaseAgent(memory=self.memory)
        self.terms = TerminologyAgent(data_dir=data_dir, memory=self.memory)
        self.enrich = EnrichmentScriptAgent(data_dir=data_dir, memory=self.memory)

    def run_enrichment_cycle(self, user_goal: str, disease_or_class: Optional[str] = None) -> Dict[str, Any]:
        self.memory.add("user", {"goal": user_goal, "target": disease_or_class})
        plan = self.llm.plan(user_goal, disease_or_class)
        self.memory.add("planner", plan)
        read = self.reader.read(disease_or_class or user_goal)
        self.memory.add("ontology_reader", read)
        kb = self.kb.gather(disease_or_class or read.get("focus_label") or user_goal)
        self.memory.add("knowledge", kb)
        maps = self.terms.map_terms(kb.get("entities") or plan.get("entities") or [user_goal])
        self.memory.add("terminologies", maps)
        script = self.enrich.generate(ontology_context=read, evidence=kb, mappings=maps, user_goal=user_goal, disease_or_class=disease_or_class)
        self.memory.add("enrichment_script", script)
        return {"plan": plan, "ontology_reader": read, "knowledge": kb, "terminologies": maps, "enrichment_script": script}
