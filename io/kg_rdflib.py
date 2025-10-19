from rdflib import Graph

class KGClient:
    def __init__(self, path: str):
        self.graph = Graph()
        self.graph.parse(path, format="turtle")
    def query(self, sparql: str):
        return list(self.graph.query(sparql))
    def labels_containing(self, phrase: str):
        q = f"""
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        SELECT ?s ?l WHERE {{
          ?s rdfs:label ?l .
          FILTER(CONTAINS(LCASE(STR(?l)), "{phrase.lower()}"))
        }} LIMIT 25
        """
        return [(str(s), str(l)) for (s,l) in self.query(q)]
