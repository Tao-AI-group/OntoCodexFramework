
from typing import Dict, Any, Optional, List, Tuple
import os, hashlib
from rdflib import Graph, URIRef, RDF, RDFS, Namespace

OWL = Namespace("http://www.w3.org/2002/07/owl#")
IAO = Namespace("http://purl.obolibrary.org/obo/IAO_")
OCX = Namespace("http://ontocodex.ai/schema#")

def _sha256(path: str) -> Optional[str]:
    try:
        h = hashlib.sha256()
        with open(path, "rb") as f:
            for chunk in iter(lambda: f.read(8192), b""):
                h.update(chunk)
        return h.hexdigest()
    except Exception:
        return None

class OntologyReaderAgent:
    def __init__(self, data_dir: str, memory):
        self.data_dir = data_dir
        self.memory = memory

    def _parse(self, path: Optional[str]) -> Graph:
        g = Graph()
        if path and os.path.exists(path) and os.path.getsize(path) > 0:
            try:
                g.parse(path)
            except Exception:
                try:
                    g.parse(path, format="turtle")
                except Exception:
                    pass
        return g

    def _classes(self, g: Graph) -> List[Tuple[str, str]]:
        out = []
        for s in g.subjects(RDF.type, OWL.Class):
            label = g.value(s, RDFS.label)
            out.append((str(s), str(label) if label else ""))
        return out

    def _object_properties(self, g: Graph) -> List[Tuple[str, str]]:
        out = []
        for s in g.subjects(RDF.type, OWL.ObjectProperty):
            label = g.value(s, RDFS.label)
            out.append((str(s), str(label) if label else ""))
        return out

    def _definitions(self, g: Graph, iri: str) -> Optional[str]:
        d = g.value(URIRef(iri), IAO["0000115"])
        return str(d) if d else None

    def _infer_requested_relations(self, props: List[Tuple[str,str]]) -> List[str]:
        labels = [p[1].lower() for p in props if p[1]]
        likely = []
        for candidate in ["treated_with","has_symptom","diagnosed_by","has_risk_factor","has_lab_test"]:
            if any(candidate.replace("_"," ") in l for l in labels) or any(candidate in l for l in labels):
                likely.append(candidate)
        return likely

    def read_from_file(self, file_path: Optional[str], requested_relations: Optional[List[str]] = None) -> Dict[str, Any]:
        g = self._parse(file_path)
        classes = self._classes(g)
        props = self._object_properties(g)
        req = requested_relations or self._infer_requested_relations(props)
        focus_iri, focus_label = (classes[0] if classes else (None, None))
        prov = {
            "file_path": file_path,
            "file_exists": os.path.exists(file_path) if file_path else False,
            "file_size": os.path.getsize(file_path) if file_path and os.path.exists(file_path) else 0,
            "sha256": _sha256(file_path) if file_path and os.path.exists(file_path) else None,
            "triple_count": len(g)
        }
        return {
            "source_file": file_path,
            "provenance": prov,
            "classes": [{"iri": c, "label": l, "definition": self._definitions(g, c)} for c, l in classes],
            "object_properties": [{"iri": p, "label": l} for p, l in props],
            "relations_to_enrich": req,
            "focus_iri": focus_iri,
            "focus_label": focus_label
        }
