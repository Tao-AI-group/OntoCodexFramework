
# OntoCodex v2.3 — Integration Patch

Implements the three requested upgrades:
1) **TerminologyAgent** — provenance + confidence (normalized score × table priority).
2) **LLMAgent** — goal decomposition (via existing planner) + **confidence harmonization** across agents.
3) **OntologyReaderAgent** — **provenance** for user OWL files (path, size, sha256, triple count).

## Apply
```bash
unzip ontocodex_v2_3_integration_patch.zip -d your_ontocodex_repo/
```

## Run example
```bash
export ONTOCODEX_DATA_DIR=./data
# Provide a user ontology at $ONTOCODEX_USER_ONTOLOGY or copy your_ontocodex_repo/examples/sample_user_ontology.ttl to ./data/user_ontology.ttl
python your_ontocodex_repo/examples/run_enrichment_v23.py
```

Outputs include harmonized confidences on relations and provenance at each stage.
