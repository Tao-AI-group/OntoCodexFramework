class Reasoner:
    """Stub for OWL reasoner; extend to ELK/HermiT sidecar."""
    def entails(self, axiom: str) -> bool:
        return False
    def subclasses(self, iri: str):
        return []
    def validate_axioms(self, axioms: list[str]) -> dict:
        return {"valid": [], "invalid": axioms}
