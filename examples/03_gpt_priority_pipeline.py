from ontocodex.kb.priority import KBConfig
from ontocodex.retrieval.priority_retriever import PriorityRetriever
from ontocodex.mapping.fuzzy import load_mapping_csv, fuzzy_map
from ontocodex.agents.guideline_augmentor import GuidelineAugmentor
from ontocodex.chains.evidence import EvidenceEnforcer
import os

DATA = os.path.join(os.path.dirname(__file__), "..", "data")

cfg = KBConfig(
    doid_path=os.path.join(DATA, "DOID.owl"),
    medlineplus_path=os.path.join(DATA, "MEDLINEPLUS.ttl"),
    hp_path=os.path.join(DATA, "HP.csv"),
    use_bioportal=False,
    use_pubmed=False
)

retriever = PriorityRetriever(cfg)
augmentor = GuidelineAugmentor(use_pubmed=False)
enforcer = EvidenceEnforcer(strict=True)

query = "Osteoarthritis"
concept = retriever.invoke(query)
concept = augmentor.invoke(concept)

tables = []
for fname, name, label_col, code_col, pr in [
    ("snomed_omop.csv","SNOMED","concept_name","concept_code", 2),
    ("rxnorm_omop.csv","RxNorm","concept_name","concept_code", 1),
    ("loinc_omop.csv","LOINC","concept_name","concept_code", 3),
]:
    path = os.path.join(DATA, fname)
    if os.path.exists(path) and os.path.getsize(path)>0:
        tables.append(load_mapping_csv(path, name, label_col, code_col, pr))

if tables:
    ranked = fuzzy_map(query, tables, limit=5)
    concept["mappings"] = ranked
    concept["top_mapping"] = ranked[0] if ranked else None

ev = []
if concept.get("definition"):
    ev.append({"text": concept["definition"], "source": concept.get("source",""), "path": "definition"})
concept["evidence"] = ev
concept = enforcer.enforce(concept)

print("=== CONCEPT ===")
for k,v in concept.items():
    print(f"{k}: {v}")
