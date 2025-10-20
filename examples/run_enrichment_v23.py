
import os, json
from ontocodex.core.orchestrator import OntoCodexOrchestrator

DATA = os.environ.get("ONTOCODEX_DATA_DIR", "data")
USER_OWL = os.environ.get("ONTOCODEX_USER_ONTOLOGY", os.path.join(DATA, "user_ontology.ttl"))

orch = OntoCodexOrchestrator(data_dir=DATA, llm_backend="auto")
res = orch.run_enrichment_cycle(
    user_goal="Enrich ontology with decomposition + provenance + harmonized confidence",
    user_ontology_path=USER_OWL,
    requested_relations=["treated_with","has_symptom","has_lab_test"]
)
print(json.dumps(res, indent=2))
print("\nScript:", res.get("enrichment_script",{}).get("script_path"))
print("TTL   :", res.get("enrichment_script",{}).get("ttl_out"))
