import os
from ontocodex.kb.priority import KBConfig
from ontocodex.multi.agents.retriever_agent import RetrieverAgent
from ontocodex.multi.agents.mapper_agent import MapperAgent
from ontocodex.multi.agents.guideline_tool_agent import GuidelineToolAgent
from ontocodex.multi.agents.validator_agent import ValidatorAgent
from ontocodex.multi.orchestrator_planned import CodexOrchestratorPlanned

DATA = os.environ.get("ONTOCODEX_DATA_DIR", "data")
cfg = KBConfig(doid_path=os.path.join(DATA,"DOID.owl"),
               medlineplus_path=os.path.join(DATA,"MEDLINEPLUS.ttl"),
               hp_path=os.path.join(DATA,"HP.csv"))

agents = [RetrieverAgent(cfg), MapperAgent(data_dir=DATA), GuidelineToolAgent(), ValidatorAgent()]
orch = CodexOrchestratorPlanned(agents)

print("— Guidelines for diabetes:")
print(orch.chat_turn("Show ADA guidelines for diabetes"))

print("\n— LOINC mapping:")
print(orch.chat_turn("Map TSH to LOINC"))

print("\n— Phenotype:")
print(orch.chat_turn("What is osteoarthritis?"))
