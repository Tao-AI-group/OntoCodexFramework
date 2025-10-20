import os
from ontocodex.kb.priority import KBConfig
from ontocodex.multi.agents.retriever_agent import RetrieverAgent
from ontocodex.multi.agents.mapper_agent import MapperAgent
from ontocodex.multi.agents.guideline_agent import GuidelineAgent
from ontocodex.multi.agents.validator_agent import ValidatorAgent
from ontocodex.multi.orchestrator_planned import CodexOrchestratorPlanned

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

orch = CodexOrchestratorPlanned(agents)

print("— Turn 1 (phenotype):")
print(orch.chat_turn("What is osteoarthritis?"))

print("\n— Turn 2 (planner routes to mapper LOINC):")
print(orch.chat_turn("Map glucose test to LOINC"))

print("\n— Turn 3 (planner routes to mapper RxNorm):")
print(orch.chat_turn("Find the RxNorm code for metformin"))

print("\n— Turn 4 (phenotype default if ambiguous):")
print(orch.chat_turn("migraine symptoms"))
