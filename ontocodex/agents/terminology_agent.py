
from typing import Dict, Any, List, Optional, Tuple
import os, csv, hashlib
from datetime import datetime, timezone
from ..utils.fuzzy import combo_similarity
from ..core.cache_manager import OCXCacheManager
from ..core.memory import ConversationMemory

VOCAB_FILES = {
    "ICD10CM": "icd10cm_omop.csv",
    "SNOMED": "snomed_omop.csv",
    "RxNorm": "rxnorm_omop.csv",
    "ATC": "atc_omop.csv",
    "LOINC": "loinc_omop.csv",
}

VOCAB_WEIGHT = {"SNOMED":1.0, "RxNorm":0.95, "LOINC":0.93, "ATC":0.90, "ICD10CM":0.88}

def _now_iso():
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00","Z")

def _sha256(path: str) -> Optional[str]:
    try:
        h = hashlib.sha256()
        with open(path, "rb") as f:
            for chunk in iter(lambda: f.read(8192), b""):
                h.update(chunk)
        return h.hexdigest()
    except Exception:
        return None

class TerminologyAgent:
    def __init__(self, data_dir: str, memory: ConversationMemory):
        self.data_dir = data_dir
        self.memory = memory
        self.cache = OCXCacheManager(os.path.expanduser("~/.ontocodex/cache/mappings"))

    def _read_rows(self, vocab: str) -> List[Dict[str,str]]:
        fn = VOCAB_FILES.get(vocab)
        if not fn:
            return []
        path = os.path.join(self.data_dir, fn)
        rows: List[Dict[str,str]] = []
        if os.path.exists(path) and os.path.getsize(path) > 0:
            try:
                with open(path, "r", encoding="utf-8") as f:
                    reader = csv.DictReader(f)
                    for r in reader:
                        rows.append(r)
            except Exception:
                pass
        return rows

    def _match(self, term: str, rows: List[Dict[str,str]]) -> Tuple[Optional[Dict[str,str]], List[Dict[str,Any]]]:
        scored = []
        name_keys = ["concept_name","name","label"]
        id_keys = ["concept_id","code","id"]
        for r in rows:
            name = next((r.get(k) for k in name_keys if r.get(k)), None)
            code = next((r.get(k) for k in id_keys if r.get(k)), None)
            if not name or not code:
                continue
            sim = combo_similarity(term, name)
            scored.append({"code": code, "label": name, "score": round(sim, 3)})
        scored.sort(key=lambda x: x["score"], reverse=True)
        top = scored[0] if scored else None
        return top, scored[:10]

    def _confidence(self, vocab: str, sim: float) -> float:
        w = VOCAB_WEIGHT.get(vocab, 0.85)
        return round(0.8 * sim + 0.2 * w, 3)

    def annotate_entities(self, entities: List[str], vocabularies: Optional[List[str]] = None) -> Dict[str, Any]:
        vocabularies = vocabularies or list(VOCAB_FILES.keys())
        all_out: Dict[str, List[Dict[str,Any]]] = {}
        mappings_flat: List[Dict[str,Any]] = []

        for ent in entities or []:
            ent_key = ent.strip()
            all_out.setdefault(ent_key, [])
            for vocab in vocabularies:
                cached = self.cache.load(f"{ent_key}|{vocab}", "mappings", max_age_days=30)
                if cached and isinstance(cached, dict) and cached.get("items"):
                    items = cached["items"]
                    for it in items:
                        it["provenance"] = it.get("provenance", {})
                        it["provenance"]["cache_used"] = True
                    all_out[ent_key].extend(items)
                    mappings_flat.extend([dict(it, term=ent_key) for it in items])
                    continue

                rows = self._read_rows(vocab)
                top, ranked = self._match(ent_key, rows)
                path = os.path.join(self.data_dir, VOCAB_FILES.get(vocab,""))
                prov = {
                    "vocabulary": vocab,
                    "mapping_file": path if os.path.exists(path) else None,
                    "mapping_file_hash": _sha256(path) if os.path.exists(path) else None,
                    "timestamp": _now_iso(),
                    "cache_used": False
                }
                if top:
                    conf = self._confidence(vocab, top["score"])
                    item = {"system": vocab, "code": top["code"], "label": top["label"], "score": top["score"], "confidence": conf, "provenance": prov}
                    all_out[ent_key].append(item)
                    mappings_flat.append(dict(item, term=ent_key))
                cache_payload = {"items": all_out[ent_key][-5:]}
                self.cache.save(f"{ent_key}|{vocab}", "mappings", cache_payload)

        return {"annotations_by_entity": all_out, "mappings": mappings_flat}
