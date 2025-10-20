import os
from ontocodex.kb.priority import KBConfig
from ontocodex.multi.agents.retriever_agent import RetrieverAgent
from ontocodex.multi.agents.mapper_agent import MapperAgent
from ontocodex.multi.agents.guideline_agent import GuidelineAgent
from ontocodex.multi.agents.validator_agent import ValidatorAgent
from ontocodex.multi.orchestrator import CodexOrchestrator

DATA = os.environ.get("ONTOCODEX_DATA_DIR","data")

cfg = KBConfig(
    doid_path=os.path.join(DATA, "DOID.owl"),
    medlineplus_path=os.path.join(DATA, "MEDLINEPLUS.ttl"),
    hp_path=os.path.join(DATA, "HP.csv"),
)

agents = [
    RetrieverAgent(cfg),
    MapperAgent(data_dir=DATA),
    GuidelineAgent(),
    ValidatorAgent(),
]

orch = CodexOrchestrator(agents)

print("=== QUERY: Osteoarthritis ===")
orch.submit("Osteoarthritis")
out1 = orch.run(max_rounds=3)
print(out1["results"])

print("\n=== QUERY: Map TSH lab to LOINC ===")
orch.submit("Map TSH lab to LOINC")
out2 = orch.run(max_rounds=3)
print(out2["results"])

print("\n=== QUERY: What are ADA guidelines for diabetes? ===")
orch.submit("What are ADA guidelines for diabetes?")
out3 = orch.run(max_rounds=3)
print(out3["results"])
