from typing import Dict, Any, Optional, List
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
        self.kb = KnowledgebaseAgent(memory=self.memory, data_dir=data_dir)
        self.terms = TerminologyAgent(data_dir=data_dir, memory=self.memory)
        self.enrich = EnrichmentScriptAgent(data_dir=data_dir, memory=self.memory)

    def run_enrichment_cycle(self, user_goal: str, user_ontology_path: Optional[str] = None, requested_relations: Optional[List[str]] = None) -> Dict[str, Any]:
        self.memory.add("user", {"goal": user_goal, "ontology_path": user_ontology_path, "requested_relations": requested_relations})
        plan = self.llm.plan(user_goal, None)
        self.memory.add("planner", plan)
        read = self.reader.read_from_file(user_ontology_path, requested_relations=requested_relations)
        self.memory.add("ontology_reader", read)
        kb = self.kb.gather_from_goal(read)
        self.memory.add("knowledge", kb)
        maps = self.terms.map_terms(kb.get("entities") or [])
        self.memory.add("terminologies", maps)
        script = self.enrich.generate(ontology_context={"focus_iri": read.get("focus_iri"), "focus_label": read.get("focus_label")}, evidence=kb, mappings=maps, user_goal=user_goal, disease_or_class=read.get("focus_label"))
        self.memory.add("enrichment_script", script)
        return {"plan": plan, "ontology_reader": read, "knowledge": kb, "terminologies": maps, "enrichment_script": script}
