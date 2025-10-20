import os, json
from ontocodex.core.orchestrator import OntoCodexOrchestrator
DATA = os.environ.get("ONTOCODEX_DATA_DIR", "data")
orch = OntoCodexOrchestrator(data_dir=DATA, llm_backend="auto")
res = orch.run_enrichment_cycle("Enrich ontology with diabetes guideline treatments", "diabetes")
print(json.dumps(res, indent=2))
