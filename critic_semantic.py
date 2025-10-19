class OntologyCritic:
    def __init__(self, kg):
        self.kg = kg

    def invoke(self, answer: dict | str):
        text = answer if isinstance(answer, str) else answer.get("content","")
        # Very light check: ensure at least one KG label appears in the answer (demo)
        labels = [l for _, l in self.kg.labels_containing("")]
        ok = any(l in text for l in labels[:50])
        return "✅ Ontology-consistent (heuristic)." if ok else "⚠️ Could not verify ontology terms."
