import os
from ontocodex.kb.priority import KBConfig
from ontocodex.retrieval.priority_retriever import PriorityRetriever
from ontocodex.chains.evidence import EvidenceEnforcer
from ontocodex.mapping.tools import MappingTool
from ontocodex.core.memory import ConversationMemory
from ontocodex.agents.onto_agent import OntoCodexAgent
DATA=os.environ.get('ONTOCODEX_DATA_DIR','data')
cfg=KBConfig(doid_path=os.path.join(DATA,'DOID.owl'), medlineplus_path=os.path.join(DATA,'MEDLINEPLUS.ttl'), hp_path=os.path.join(DATA,'HP.csv'))
agent=OntoCodexAgent(PriorityRetriever(cfg), EvidenceEnforcer(True), MappingTool(), ConversationMemory(), data_dir=DATA)
print(agent.invoke('What is osteoarthritis?'))
print(agent.invoke('Map glucose test to LOINC'))
print(agent.invoke('Find RxNorm code for metformin'))
