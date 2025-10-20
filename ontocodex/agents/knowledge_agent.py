from typing import Dict, Any, List, Optional, Tuple
import os
from datetime import datetime, timezone
from rdflib import Graph, RDFS, Namespace
from ..guidelines.guideline_retrievers import (
    pubmed_guidelines, ada_guidelines, acc_guidelines, aha_guidelines, nih_guidelines, cdc_guidelines
)

SKOS = Namespace("http://www.w3.org/2004/02/skos/core#")
IAO = Namespace("http://purl.obolibrary.org/obo/IAO_")

def _now_iso():
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00","Z")

class KnowledgebaseAgent:
    def __init__(self, memory, data_dir: str = "data"):
        self.memory = memory
        self.data_dir = data_dir
        self.mlp_ttl = os.path.join(self.data_dir, "MEDLINEPLUS.ttl")
        self.doid_ttl = os.path.join(self.data_dir, "DOID.ttl")
        self.doid_owl = os.path.join(self.data_dir, "DOID.owl")

    def _parse_if_exists(self, path: str) -> Graph:
        g = Graph()
        if os.path.exists(path) and os.path.getsize(path) > 0:
            try:
                g.parse(path)
            except Exception:
                try:
                    g.parse(path, format="turtle")
                except Exception:
                    pass
        return g

    def _extract_from_definition(self, text: str, requested: List[str]) -> List[Dict[str,Any]]:
        t = (text or "").lower()
        rels: List[Dict[str,Any]] = []
        hits = 0
        if "insulin" in t and "treated_with" in requested:
            rels.append({"predicate":"treated_with","object":"Insulin"}); hits += 1
        if any(k in t for k in ["polyuria","polydipsia","weight loss"]) and "has_symptom" in requested:
            rels.append({"predicate":"has_symptom","object":"Polyuria"}); hits += 1
        if ("glycated hemoglobin" in t or "hba1c" in t) and "has_lab_test" in requested:
            rels.append({"predicate":"has_lab_test","object":"HbA1c"}); hits += 1
        for r in rels:
            r["hits"] = hits
        return rels

    def _lookup_mlp(self, label: Optional[str]): 
        if not label: return None, [], None
        g = self._parse_if_exists(self.mlp_ttl)
        if len(g) == 0: return None, [], None
        for s, l in g.subject_objects(RDFS.label):
            if str(l).lower() == label.lower():
                d = g.value(s, SKOS.definition)
                return (str(d) if d else None), [{"source":"MedlinePlus","uri":str(s)}], str(s)
        return None, [], None

    def _lookup_doid(self, label: Optional[str]): 
        if not label: return None, [], None
        g = self._parse_if_exists(self.doid_ttl)
        if len(g) == 0:
            g = self._parse_if_exists(self.doid_owl)
        if len(g) == 0: return None, [], None
        for s, l in g.subject_objects(RDFS.label):
            if str(l).lower() == label.lower():
                d = g.value(s, IAO["0000115"])
                return (str(d) if d else None), [{"source":"DOID","uri":str(s)}], str(s)
        return None, [], None

    def _conf_text(self, base: float, hits: int) -> float:
        return round(min(base + 0.03 * max(hits, 0), 0.98), 3)

    def _conf_guideline(self, base: float, year: Optional[int]) -> float:
        from datetime import datetime
        y = datetime.utcnow().year
        if year and year >= y - 2:
            base += 0.02
        return round(min(base, 0.98), 3)

    def gather_from_goal(self, reader_goal: Dict[str, Any]) -> Dict[str, Any]:
        focus_label = reader_goal.get("focus_label")
        requested = reader_goal.get("relations_to_enrich") or []
        out_rels: List[Dict[str, Any]] = []
        evidence_snips: List[str] = []
        entities: List[str] = []

        mlp_def, _, mlp_uri = self._lookup_mlp(focus_label)
        if mlp_def:
            mined = self._extract_from_definition(mlp_def, requested)
            for m in mined:
                m.update({
                    "source": "MedlinePlus",
                    "source_uri": mlp_uri,
                    "evidence": mlp_def,
                    "agent": "KnowledgebaseAgent",
                    "timestamp": _now_iso(),
                    "confidence": self._conf_text(0.90, m.get("hits", 0)),
                })
            out_rels.extend(mined)
            evidence_snips.append(mlp_def)
            entities.extend([m["object"] for m in mined])

        if len(out_rels) < len(requested):
            doid_def, _, doid_uri = self._lookup_doid(focus_label)
            if doid_def:
                mined = self._extract_from_definition(doid_def, requested)
                for m in mined:
                    m.update({
                        "source": "DOID",
                        "source_uri": doid_uri,
                        "evidence": doid_def,
                        "agent": "KnowledgebaseAgent",
                        "timestamp": _now_iso(),
                        "confidence": self._conf_text(0.75, m.get("hits", 0)),
                    })
                seen = {(r["predicate"], r["object"]) for r in out_rels}
                for m in mined:
                    if (m["predicate"], m["object"]) not in seen:
                        out_rels.append(m); seen.add((m["predicate"], m["object"]))
                evidence_snips.append(doid_def)
                entities.extend([m["object"] for m in mined])

        if focus_label:
            pm = pubmed_guidelines(focus_label, max_results=5)
            for rec in pm:
                out_rels.append({
                    "predicate": "supported_by_guideline",
                    "object": f"PubMed:{rec.get('pmid')}",
                    "source": "PubMed",
                    "source_uri": rec.get("url"),
                    "evidence": rec.get("title"),
                    "agent": "KnowledgebaseAgent",
                    "timestamp": _now_iso(),
                    "confidence": self._conf_guideline(0.85, rec.get("year"))
                })
                evidence_snips.append(rec.get("title") or "")

        inst_sources = [("ADA", ada_guidelines), ("ACC", acc_guidelines), ("AHA", aha_guidelines), ("NIH", nih_guidelines), ("CDC", cdc_guidelines)]
        for name, fn in inst_sources:
            try:
                recs = fn(focus_label or "")
            except Exception:
                recs = []
            for rec in recs[:2]:
                out_rels.append({
                    "predicate": "supported_by_guideline",
                    "object": f"{name}:{rec.get('year')}",
                    "source": name,
                    "source_uri": rec.get("url"),
                    "evidence": rec.get("title"),
                    "agent": "KnowledgebaseAgent",
                    "timestamp": _now_iso(),
                    "confidence": self._conf_guideline(0.88, rec.get("year"))
                })
                evidence_snips.append(rec.get("title") or "")

        return {"focus_label": focus_label, "relations": out_rels, "evidence_snippets": [e for e in evidence_snips if e], "entities": list(dict.fromkeys(entities)), "source_priority": ["MedlinePlus", "DOID.ttl/DOID.owl", "PubMed(≤5y)", "ADA/ACC/AHA/NIH/CDC"]}
