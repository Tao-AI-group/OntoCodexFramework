from typing import Dict, Any, List, Optional, Tuple
import os
from rdflib import Graph, RDFS, Namespace
SKOS = Namespace("http://www.w3.org/2004/02/skos/core#")
IAO = Namespace("http://purl.obolibrary.org/obo/IAO_")
class KnowledgebaseAgent:
    def __init__(self, memory, data_dir: str = "data"):
        self.memory = memory; self.data_dir = data_dir
        self.mlp_ttl = os.path.join(self.data_dir, "MEDLINEPLUS.ttl")
        self.doid_ttl = os.path.join(self.data_dir, "DOID.ttl")
        self.doid_owl = os.path.join(self.data_dir, "DOID.owl")
    def _parse_if_exists(self, path: str) -> Graph:
        g = Graph()
        if os.path.exists(path) and os.path.getsize(path) > 0:
            try: g.parse(path)
            except Exception:
                try: g.parse(path, format="turtle")
                except Exception: pass
        return g
    def _extract_from_definition(self, text: str, requested: List[str]) -> List[Dict[str,str]]:
        t=text.lower(); rels=[]
        if "insulin" in t and "treated_with" in requested: rels.append({"predicate":"treated_with","object":"Insulin"})
        if any(k in t for k in ["polyuria","polydipsia","weight loss"]) and "has_symptom" in requested: rels.append({"predicate":"has_symptom","object":"Polyuria"})
        if "glycated hemoglobin" in t and "has_lab_test" in requested: rels.append({"predicate":"has_lab_test","object":"HbA1c"})
        return rels
    def _lookup_mlp(self, label: Optional[str]): 
        if not label: return None, []
        g=self._parse_if_exists(self.mlp_ttl); 
        if len(g)==0: return None, []
        for s,l in g.subject_objects(RDFS.label):
            if str(l).lower()==label.lower():
                d=g.value(s, SKOS.definition); return (str(d) if d else None), [{"source":"MedlinePlus","uri":str(s)}]
        return None, []
    def _lookup_doid(self, label: Optional[str]): 
        if not label: return None, []
        g=self._parse_if_exists(self.doid_ttl); 
        if len(g)==0: g=self._parse_if_exists(self.doid_owl)
        if len(g)==0: return None, []
        for s,l in g.subject_objects(RDFS.label):
            if str(l).lower()==label.lower():
                d=g.value(s, IAO["0000115"]); return (str(d) if d else None), [{"source":"DOID","uri":str(s)}]
        return None, []
    def gather_from_goal(self, reader_goal: Dict[str, Any]) -> Dict[str, Any]:
        focus_label=reader_goal.get("focus_label"); requested=reader_goal.get("relations_to_enrich") or []
        out_rels=[]; evidence=[]; entities=[]
        mlp_def, mlp_meta = self._lookup_mlp(focus_label)
        if mlp_def:
            mined=self._extract_from_definition(mlp_def, requested)
            for m in mined: m["source"]="MedlinePlus"
            out_rels.extend(mined); evidence.append(mlp_def); entities.extend([m["object"] for m in mined])
        if not mlp_def or len(out_rels) < len(requested):
            doid_def, doid_meta = self._lookup_doid(focus_label)
            if doid_def:
                mined=self._extract_from_definition(doid_def, requested)
                for m in mined: m["source"]="DOID"
                for m in mined:
                    if m not in out_rels: out_rels.append(m)
                evidence.append(doid_def); entities.extend([m["object"] for m in mined])
        return {"focus_label":focus_label,"relations":out_rels,"evidence_snippets":evidence,"entities":list(dict.fromkeys(entities)),"source_priority":["MedlinePlus","DOID.ttl/DOID.owl"]}
