# OntoCodex v2.1 — User Ontology Reader + Knowledgebase Priority Patch
- Reader: parses user OWL/TTL and extracts classes, properties, and requested relations.
- Knowledgebase: prioritizes MedlinePlus (API/TTL) then DOID.ttl (fallback to DOID.owl).
- Orchestrator: wires reader goal → knowledgebase → terminology → enrichment script.
Usage:
  export ONTOCODEX_DATA_DIR=./data
  # optionally copy examples/sample_user_ontology.ttl to ./data/user_ontology.ttl
  python examples/run_enrichment_from_user_ontology.py
