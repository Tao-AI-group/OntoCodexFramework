import os
from ontocodex.kb.priority import KBConfig
from ontocodex.retrieval.priority_retriever import PriorityRetriever
from ontocodex.chains.evidence import EvidenceEnforcer
from ontocodex.mapping.tools import MappingTool
from ontocodex.core.memory import ConversationMemory
from ontocodex.agents.onto_agent import OntoCodexAgent

DATA = os.environ.get("ONTOCODEX_DATA_DIR","data")

cfg = KBConfig(
    doid_path=os.path.join(DATA, "DOID.owl"),
    medlineplus_path=os.path.join(DATA, "MEDLINEPLUS.ttl"),
    hp_path=os.path.join(DATA, "HP.csv"),
)

memory = ConversationMemory(max_turns=20)
agent = OntoCodexAgent(
    retriever=PriorityRetriever(cfg),
    enforcer=EvidenceEnforcer(strict=True),
    mapper=MappingTool(),
    memory=memory,
    data_dir=DATA
)

print("Turn 1:", agent.invoke("What is osteoarthritis?"))
print("Turn 2:", agent.invoke("Map to LOINC: TSH"))
print("Turn 3:", agent.invoke("best code for metformin in RxNorm"))
print("History prompt:\n", memory.to_prompt())
