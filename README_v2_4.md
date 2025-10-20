# OntoCodex v2.4 — PubMed + ADA/ACC/AHA/NIH/CDC Integration

KnowledgebaseAgent now consults additional sources with 5-year recency for PubMed.

## Source Priority
1) MedlinePlus (local TTL/API)
2) DOID.ttl / DOID.owl
3) PubMed (≤5 years)
4) ADA, ACC, AHA, NIH, CDC institutional sources

All results carry provenance and confidence. PubMed/Institutional retrievers live in:
`ontocodex/guidelines/guideline_retrievers.py` (urllib-only).

## Try the example
```bash
unzip ontocodex_v2_4_guidelines_patch.zip -d your_ontocodex_repo/
export ONTOCODEX_DATA_DIR=./data
python your_ontocodex_repo/examples/run_enrichment_v24_guidelines.py
```
