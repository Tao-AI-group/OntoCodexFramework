from typing import Dict, Any, Optional, List, Tuple
import os
from rdflib import Graph, URIRef, RDF, RDFS, Namespace

OWL = Namespace("http://www.w3.org/2002/07/owl#")
IAO = Namespace("http://purl.obolibrary.org/obo/IAO_")
OCX = Namespace("http://ontocodex.ai/schema#")

class OntologyReaderAgent:
    def __init__(self, data_dir: str, memory):
        self.data_dir = data_dir
        self.memory = memory
    def _parse(self, path: Optional[str]) -> Graph:
        g = Graph()
        if path and os.path.exists(path) and os.path.getsize(path) > 0:
            try: g.parse(path)
            except Exception:
                try: g.parse(path, format="turtle")
                except Exception: pass
        return g
    def _classes(self, g: Graph) -> List[Tuple[str, str]]:
        out=[]; 
        for s in g.subjects(RDF.type, OWL.Class):
            label=g.value(s, RDFS.label); out.append((str(s), str(label) if label else ""))
        return out
    def _object_properties(self, g: Graph) -> List[Tuple[str, str]]:
        out=[]; 
        for s in g.subjects(RDF.type, OWL.ObjectProperty):
            label=g.value(s, RDFS.label); out.append((str(s), str(label) if label else ""))
        return out
    def _definitions(self, g: Graph, iri: str) -> Optional[str]:
        d=g.value(URIRef(iri), IAO["0000115"]); return str(d) if d else None
    def _infer_requested_relations(self, props: List[Tuple[str,str]]) -> List[str]:
        labels=[p[1].lower() for p in props if p[1]]; likely=[]
        for cand in ["treated_with","has_symptom","diagnosed_by","has_risk_factor","has_lab_test"]:
            if any(cand.replace("_"," ") in l for l in labels) or any(cand in l for l in labels): likely.append(cand)
        return likely
    def read_from_file(self, file_path: Optional[str], requested_relations: Optional[List[str]] = None) -> Dict[str, Any]:
        g=self._parse(file_path); classes=self._classes(g); props=self._object_properties(g)
        req=requested_relations or self._infer_requested_relations(props)
        focus_iri,focus_label=(classes[0] if classes else (None,None))
        return {
            "source_file": file_path,
            "classes": [{"iri": c, "label": l, "definition": self._definitions(g, c)} for c,l in classes],
            "object_properties": [{"iri": p, "label": l} for p,l in props],
            "relations_to_enrich": req,
            "focus_iri": focus_iri, "focus_label": focus_label
        }
