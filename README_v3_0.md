
# OntoCodex v3.0 — Terminology Annotation & Code Alignment

Adds a full terminology annotation layer:
- Multi-vocabulary fuzzy mapping (ICD-10-CM, SNOMED CT, RxNorm, ATC, LOINC)
- Confidence = 0.8 * similarity + 0.2 * vocab_weight (SNOMED > RxNorm > LOINC > ATC > ICD10CM)
- Cache results per (entity, vocab) in ~/.ontocodex/cache/mappings
- Enrichment script emits oboInOwl:hasDbXref per entity with PROV-O provenance

## Usage
```bash
unzip ontocodex_v3_0_annotations_patch.zip -d your_ontocodex_repo/
export ONTOCODEX_DATA_DIR=./data
python your_ontocodex_repo/examples/run_enrichment_v30_annotations.py
```

## Data files
Place CSVs in $ONTOCODEX_DATA_DIR with filenames:
- icd10cm_omop.csv
- snomed_omop.csv
- rxnorm_omop.csv
- atc_omop.csv
- loinc_omop.csv

Expected columns (flexible): one of {concept_id, code, id} and one of {concept_name, name, label}.
