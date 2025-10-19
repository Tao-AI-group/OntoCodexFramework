from pydantic import BaseModel

class SparqlArgs(BaseModel):
    query: str

class SPARQLTool:
    def __init__(self, kg_client):
        self.kg = kg_client
    def invoke(self, args: dict | SparqlArgs):
        if isinstance(args, dict):
            q = args.get("query","")
        else:
            q = args.query
        return [tuple(map(str, row)) for row in self.kg.query(q)]
