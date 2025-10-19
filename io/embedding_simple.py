import numpy as np
import hashlib

class SimpleEmbedder:
    """Deterministic bag-of-words hashing embedder (demo-safe)."""
    def __init__(self, dim: int = 256):
        self.dim = dim
    def _h(self, token: str) -> int:
        return int(hashlib.sha256(token.encode()).hexdigest(), 16) % self.dim
    def embed(self, texts):
        return [self.embed_query(t) for t in texts]
    def embed_query(self, text: str):
        vec = np.zeros(self.dim, dtype=float)
        for tok in text.lower().split():
            vec[self._h(tok)] += 1.0
        # L2 normalize
        n = np.linalg.norm(vec) or 1.0
        return (vec / n).astype(float)
