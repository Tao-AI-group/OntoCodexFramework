from ontocodex.io.embedding_simple import SimpleEmbedder
from ontocodex.io.vector_simple import SimpleVectorStore
from ontocodex.io.kg_rdflib import KGClient
from ontocodex.io.llm_openai import ChatOpenAI
from ontocodex.retrieval.hybrid import HybridRetriever
from ontocodex.chains.rag_kg import KGRAg
from ontocodex.chains.critic_semantic import OntologyCritic

# Minimal, runs offline with STUB LLM
embedder = SimpleEmbedder(dim=256)
vec = SimpleVectorStore(dim=256)
kg = KGClient(path="data/ontology.ttl")

# Seed some texts
texts = [
    "Osteoarthritis is a degenerative joint disease.",
    "Total knee arthroplasty is a surgical procedure to replace the weight-bearing surfaces of the knee joint.",
    "Risk factors include age, obesity, and prior injury."
]
vec.add([embedder.embed_query(t) for t in texts], texts)

retriever = HybridRetriever(vec, kg, embedder, k=5)
llm = ChatOpenAI(model="gpt-4o-mini", api_key=None)  # None => STUB
chain = KGRAg(retriever, llm)
critic = OntologyCritic(kg)

question = "What causes osteoarthritis and how is TKA related?"
answer = chain.invoke(question)
print("LLM Answer:", answer.get("content") if isinstance(answer, dict) else answer)
print("Critic:", critic.invoke(answer))
