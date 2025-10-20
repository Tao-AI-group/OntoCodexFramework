import os
from ontocodex.core.memory import ConversationMemory
from ontocodex.agents.planner_llm import TinyPlanner

memory = ConversationMemory(max_turns=5)
planner = TinyPlanner(memory)

print("Using LLM backend:", planner.llm.__class__.__name__)
queries = [
    "What is osteoarthritis?",
    "Map glucose test to LOINC",
    "Find the RxNorm code for metformin"
]
for q in queries:
    print("\nUser:", q)
    print("Plan:", planner.plan(q))
