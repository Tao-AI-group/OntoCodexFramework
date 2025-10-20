# OntoCodex v2.2 — Provenance & Confidence Patch

Adds W3C PROV-O provenance + heuristic confidence scores to enrichment outputs.

## Install & Run
```bash
unzip ontocodex_v2_2_provenance_patch.zip -d your_ontocodex_repo/
export ONTOCODEX_DATA_DIR=./data
python your_ontocodex_repo/examples/run_enrichment_with_provenance.py
```

## Notes
- Confidence heuristic: base 0.90 (MedlinePlus) / 0.75 (DOID) + 0.03 per keyword hit; capped at 0.98.
- TTL is written by `ontology_updates/auto_enrich_prov_<timestamp>.py` when you execute it.
