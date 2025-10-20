import os, json
from ontocodex.core.orchestrator import OntoCodexOrchestrator
DATA = os.environ.get("ONTOCODEX_DATA_DIR", "data")
USER_OWL = os.environ.get("ONTOCODEX_USER_ONTOLOGY", os.path.join(DATA, "user_ontology.ttl"))
orch = OntoCodexOrchestrator(data_dir=DATA, llm_backend="auto")
result = orch.run_enrichment_cycle(user_goal="Enrich user ontology using MedlinePlus then DOID", user_ontology_path=USER_OWL, requested_relations=["treated_with","has_symptom","has_lab_test"])
print(json.dumps(result, indent=2))
print("\nGenerated script:", result.get("enrichment_script",{}).get("script_path"))
