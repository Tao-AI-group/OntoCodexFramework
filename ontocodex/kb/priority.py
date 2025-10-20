from dataclasses import dataclass
from typing import List, Optional, Dict, Any, Tuple
import pandas as pd
from rdflib import Graph
from rdflib.namespace import RDFS
@dataclass
class KBConfig:
    doid_path: str; medlineplus_path: str; hp_path: str
    use_bioportal: bool = False; use_pubmed: bool = False
class DOIDLoader:
    def __init__(self, path: str): self.graph = Graph(); self.graph.parse(path)
    def lookup_label(self, text: str) -> List[Tuple[str,str]]:
        q=f"""PREFIX rdfs: <{RDFS}>
        SELECT ?s ?l WHERE {{ ?s rdfs:label ?l . FILTER(CONTAINS(LCASE(STR(?l)),'{text.lower()}')) }} LIMIT 50"""
        return [(str(s),str(l)) for (s,l) in self.graph.query(q)]
    def definition(self, iri: str) -> Optional[str]:
        q=f"""PREFIX IAO: <http://purl.obolibrary.org/obo/IAO_>
        SELECT ?d WHERE {{ <{iri}> IAO:0000115 ?d }} LIMIT 1"""; rows=list(self.graph.query(q)); return str(rows[0][0]) if rows else None
    def parent_child_defs(self, iri: str) -> Dict[str, List[str]]:
        out={'parents':[],'children':[]}
        qp=f"""PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX IAO: <http://purl.obolibrary.org/obo/IAO_>
        SELECT ?p ?d WHERE {{ <{iri}> rdfs:subClassOf ?p . OPTIONAL {{ ?p IAO:0000115 ?d }} }}"""
        for (p,d) in self.graph.query(qp): out['parents'].append((str(p), str(d) if d else ""))
        qc=f"""PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX IAO: <http://purl.obolibrary.org/obo/IAO_>
        SELECT ?c ?d WHERE {{ ?c rdfs:subClassOf <{iri}> . OPTIONAL {{ ?c IAO:0000115 ?d }} }}"""
        for (c,d) in self.graph.query(qc): out['children'].append((str(c), str(d) if d else ""))
        return out
class MedlinePlusLoader:
    def __init__(self, path: str): self.graph = Graph(); self.graph.parse(path, format='turtle')
    def definitions(self, text: str) -> List[str]:
        q=f"""PREFIX skos:<http://www.w3.org/2004/02/skos/core#> PREFIX rdfs:<http://www.w3.org/2000/01/rdf-schema#>
        SELECT ?def WHERE {{ ?s rdfs:label ?l ; skos:definition ?def . FILTER(CONTAINS(LCASE(STR(?l)),'{text.lower()}')) }} LIMIT 50"""
        return [str(d) for (d,) in self.graph.query(q)]
class HPTable:
    def __init__(self, path: str): import pandas as pd; self.df = pd.read_csv(path) if path else pd.DataFrame(columns=['id','label','synonym']); self.df.columns=[c.lower() for c in self.df.columns]
    def search(self, text: str): 
        if self.df.empty or 'label' not in self.df.columns: return []
        t=text.lower(); hits=self.df[self.df['label'].str.lower().str.contains(t, na=False)]; 
        return list(zip(hits['id'].astype(str), hits['label'].astype(str)))
class PriorityRouter:
    def __init__(self, cfg: KBConfig): self.cfg=cfg; self.doid=DOIDLoader(cfg.doid_path); self.mlp=MedlinePlusLoader(cfg.medlineplus_path); self.hp=HPTable(cfg.hp_path)
    def resolve_concept(self, text: str) -> Dict[str, Any]:
        h=self.doid.lookup_label(text)
        if h: iri,label=h[0]; definition=self.doid.definition(iri); ctx=self.doid.parent_child_defs(iri); return {'source':'DOID','label':label,'iri':iri,'definition':definition,'context':ctx}
        defs=self.mlp.definitions(text)
        if defs: return {'source':'MedlinePlus','label':text,'definition':defs[0]}
        hp=self.hp.search(text)
        if hp: id_,label=hp[0]; return {'source':'HP','label':label,'id':id_}
        if self.cfg.use_bioportal: return {'source':'BioPortal','label':text}
        return {'source':'UNRESOLVED','label':text}
