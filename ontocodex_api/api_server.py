from fastapi import FastAPI, Query
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import os

# Import OntoCodex modules (install your framework first)
from ontocodex.kb.priority import KBConfig
from ontocodex.retrieval.priority_retriever import PriorityRetriever
from ontocodex.mapping.fuzzy import load_mapping_csv, fuzzy_map
from ontocodex.agents.guideline_augmentor import GuidelineAugmentor
from ontocodex.chains.evidence import EvidenceEnforcer

DATA_DIR = os.environ.get("ONTOCODEX_DATA_DIR", "data")

# Initialize pipeline (BioPortal/PubMed disabled per user request)
cfg = KBConfig(
    doid_path=os.path.join(DATA_DIR, "DOID.owl"),
    medlineplus_path=os.path.join(DATA_DIR, "MEDLINEPLUS.ttl"),
    hp_path=os.path.join(DATA_DIR, "HP.csv"),
    use_bioportal=False,
    use_pubmed=False
)

retriever = PriorityRetriever(cfg)
augmentor = GuidelineAugmentor(use_pubmed=False)
enforcer = EvidenceEnforcer(strict=True)

def _load_tables(which: List[str]):
    tables = []
    for name in which:
        if name.lower() == "rxnorm":
            path, label_col, code_col, pr = os.path.join(DATA_DIR, "rxnorm_omop.csv"), "concept_name", "concept_code", 1
        elif name.lower() == "snomed":
            path, label_col, code_col, pr = os.path.join(DATA_DIR, "snomed_omop.csv"), "concept_name", "concept_code", 2
        elif name.lower() == "loinc":
            path, label_col, code_col, pr = os.path.join(DATA_DIR, "loinc_omop.csv"), "concept_name", "concept_code", 3
        else:
            continue
        if os.path.exists(path) and os.path.getsize(path) > 0:
            tables.append(load_mapping_csv(path, name.upper(), label_col, code_col, pr))
    return tables

app = FastAPI(title="OntoCodex API", version="0.2.0", docs_url="/docs", redoc_url=None)

@app.get("/ping")
def ping():
    return {"ok": True, "message": "OntoCodex API alive"}

@app.get("/phenotype")
def phenotype(disease: str = Query(..., description="Disease label to resolve via DOID priority routing")):
    concept = retriever.invoke(disease)
    # attach evidence
    ev = []
    if concept.get("definition"):
        ev.append({"text": concept["definition"], "source": concept.get("source",""), "path": "definition"})
    concept["evidence"] = ev
    concept = enforcer.enforce(concept)
    return {"query": disease, "concept": concept}

@app.get("/map/lab")
def map_lab(term: str = Query(..., description="Lab test text to map to LOINC")):
    tables = _load_tables(["loinc"])
    ranked = fuzzy_map(term, tables, limit=10) if tables else []
    top = ranked[0] if ranked else None
    return {"query": term, "target": "LOINC", "ranked": ranked, "top": top}

@app.get("/map/treatment")
def map_treatment(term: str = Query(..., description="Treatment/Drug text to map to RxNorm")):
    tables = _load_tables(["rxnorm"])
    ranked = fuzzy_map(term, tables, limit=10) if tables else []
    top = ranked[0] if ranked else None
    return {"query": term, "target": "RxNorm", "ranked": ranked, "top": top}

@app.get("/map/symptom")
def map_symptom(term: str = Query(..., description="Symptom/Phenotype text to map to SNOMED")):
    tables = _load_tables(["snomed"])
    ranked = fuzzy_map(term, tables, limit=10) if tables else []
    top = ranked[0] if ranked else None
    return {"query": term, "target": "SNOMED", "ranked": ranked, "top": top}

@app.get("/guidelines")
def guidelines(disease: str = Query(..., description="Disease label for guideline augmentation")):
    concept = retriever.invoke(disease)
    concept = augmentor.invoke(concept)  # PubMed disabled; adds ADA/ACC/AHA/NIH/CDC stubs
    return {"query": disease, "guidelines": concept.get("guidelines", []), "source": concept.get("source")}
