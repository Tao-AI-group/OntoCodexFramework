import numpy as np
from typing import List, Tuple, Any

class SimpleVectorStore:
    def __init__(self, dim: int):
        self.dim = dim
        self.embs: List[np.ndarray] = []
        self.texts: List[str] = []

    def add(self, embeddings: List[np.ndarray], texts: List[str]):
        for e, t in zip(embeddings, texts):
            self.embs.append(np.array(e, dtype=float))
            self.texts.append(t)

    def similarity_search(self, query_emb: np.ndarray, k: int = 5):
        if not self.embs:
            return []
        E = np.stack(self.embs, axis=0)
        # cosine similarity
        q = query_emb / (np.linalg.norm(query_emb) or 1.0)
        E = E / (np.linalg.norm(E, axis=1, keepdims=True) + 1e-9)
        sims = E @ q
        idx = np.argsort(-sims)[:k]
        return [self.texts[i] for i in idx]
