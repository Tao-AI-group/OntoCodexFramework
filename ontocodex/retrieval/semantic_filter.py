from typing import List

class SemanticFilter:
    """Placeholder for OWL/SHACL-based document filtering."""
    def __init__(self, allowed_keywords: List[str] | None = None):
        self.allowed = [k.lower() for k in (allowed_keywords or [])]

    def invoke(self, docs: List[str]) -> List[str]:
        if not self.allowed:
            return docs
        return [d for d in docs if any(k in d.lower() for k in self.allowed)]
