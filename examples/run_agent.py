import os
from ontocodex.kb.priority import KBConfig
from ontocodex.retrieval.priority_retriever import PriorityRetriever
from ontocodex.chains.evidence import EvidenceEnforcer
from ontocodex.mapping.tools import MappingTool
from ontocodex.agents.onto_agent import OntoCodexAgent

DATA = os.environ.get("ONTOCODEX_DATA_DIR","data")

cfg = KBConfig(
    doid_path=os.path.join(DATA, "DOID.owl"),
    medlineplus_path=os.path.join(DATA, "MEDLINEPLUS.ttl"),
    hp_path=os.path.join(DATA, "HP.csv"),
)

retriever = PriorityRetriever(cfg)
enforcer = EvidenceEnforcer(strict=True)
mapper = MappingTool()

agent = OntoCodexAgent(retriever, enforcer, mapper)

print("— Phenotype —")
print(agent.invoke("phenotype disease", {"term":"Osteoarthritis"}))

print("\n— Map RxNorm —")
print(agent.invoke("map code", {"term":"metformin", "table":"rxnorm", "limit":5, "data_dir":DATA}))

print("\n— Map LOINC —")
print(agent.invoke("map lab", {"term":"TSH", "table":"loinc", "limit":5, "data_dir":DATA}))
