from ontocodex.io.llm_openai import ChatOpenAI
from ontocodex.io.embedding_simple import SimpleEmbedder
from ontocodex.io.vector_simple import SimpleVectorStore
from ontocodex.io.kg_rdflib import KGClient
from ontocodex.retrieval.hybrid import HybridRetriever
from ontocodex.agents.planner_onto import OntologyPlanner
from ontocodex.agents.tools import SPARQLTool

embedder = SimpleEmbedder(dim=128)
vec = SimpleVectorStore(dim=128)
kg = KGClient(path="data/ontology.ttl")
vec.add([embedder.embed_query("Osteoarthritis basics")], ["Osteoarthritis basics"])

llm = ChatOpenAI(api_key=None)  # STUB
tools = {
    "retriever": HybridRetriever(vec, kg, embedder),
    "sparql": SPARQLTool(kg),
}
planner = OntologyPlanner(llm, tools)

print("Planner (retrieve):", planner.invoke("Explain osteoarthritis briefly."))
print("Planner (sparql):", planner.invoke("Find labels via KG. Use SPARQL: SELECT ?l WHERE { ?s <http://www.w3.org/2000/01/rdf-schema#label> ?l }"))
