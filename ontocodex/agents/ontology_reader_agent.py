from typing import Dict, Any, Optional, List, Tuple
import os
from rdflib import Graph
from rdflib.namespace import RDFS
from ..core.memory import ConversationMemory

class OntologyReaderAgent:
    def __init__(self, data_dir: str, memory: ConversationMemory, doid_filename: str = "DOID.owl"):
        self.data_dir = data_dir
        self.doid_path = os.path.join(data_dir, doid_filename)
        self.memory = memory
        self.graph = Graph()
        try:
            if os.path.exists(self.doid_path) and os.path.getsize(self.doid_path) > 0:
                self.graph.parse(self.doid_path)
        except Exception:
            pass

    def _search_label(self, text: str, limit: int = 25) -> List[Tuple[str,str]]:
        if len(self.graph) == 0:
            return []
        q = f"""PREFIX rdfs: <{RDFS}>
        SELECT ?s ?l WHERE {{
          ?s rdfs:label ?l .
          FILTER(CONTAINS(LCASE(STR(?l)), "{text.lower()}"))
        }} LIMIT {limit}"""
        return [(str(s), str(l)) for (s,l) in self.graph.query(q)]

    def _definition(self, iri: str) -> Optional[str]:
        if len(self.graph) == 0:
            return None
        q = f"""PREFIX IAO: <http://purl.obolibrary.org/obo/IAO_>
        SELECT ?d WHERE {{ <{iri}> IAO:0000115 ?d }} LIMIT 1"""
        rows = list(self.graph.query(q))
        return str(rows[0][0]) if rows else None

    def _neighbors(self, iri: str) -> Dict[str, Any]:
        if len(self.graph) == 0:
            return {"parents": [], "children": []}
        qp = f"""PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX IAO: <http://purl.obolibrary.org/obo/IAO_>
        SELECT ?p ?d WHERE {{ <{iri}> rdfs:subClassOf ?p . OPTIONAL {{ ?p IAO:0000115 ?d }} }}"""
        parents = [(str(p), str(d) if d else "") for (p,d) in self.graph.query(qp)]
        qc = f"""PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX IAO: <http://purl.obolibrary.org/obo/IAO_>
        SELECT ?c ?d WHERE {{ ?c rdfs:subClassOf <{iri}> . OPTIONAL {{ ?c IAO:0000115 ?d }} }}"""
        children = [(str(c), str(d) if d else "") for (c,d) in self.graph.query(qc)]
        return {"parents": parents, "children": children}

    def read(self, focus_text: str) -> Dict[str, Any]:
        hits = self._search_label(focus_text)
        if hits:
            iri, label = hits[0]
            definition = self._definition(iri)
            ctx = self._neighbors(iri)
            return {"source":"DOID","focus_iri":iri,"focus_label":label,"definition":definition,"neighbors":ctx}
        return {"source":"DOID","focus_label":focus_text,"hits":[]}
