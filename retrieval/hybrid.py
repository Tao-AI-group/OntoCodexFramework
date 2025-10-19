from typing import List
from ..io.embedding_simple import SimpleEmbedder

class HybridRetriever:
    def __init__(self, vectorstore, kg, embedder: SimpleEmbedder, k: int = 5):
        self.vec = vectorstore
        self.kg = kg
        self.embed = embedder
        self.k = k

    def invoke(self, query: str) -> List[str]:
        q_emb = self.embed.embed_query(query)
        vec_docs = self.vec.similarity_search(q_emb, k=self.k)
        kg_hits = self.kg.labels_containing(query)
        kg_docs = [f"{iri} :: {label}" for iri, label in kg_hits]
        # simple dedupe preserving order
        seen = set()
        merged = []
        for d in vec_docs + kg_docs:
            if d not in seen:
                seen.add(d)
                merged.append(d)
        return merged
