from typing import Dict, Any

class GuidelineAugmentor:
    def __init__(self, use_pubmed: bool = False):
        self.use_pubmed = use_pubmed
    def invoke(self, concept: Dict[str, Any]) -> Dict[str, Any]:
        concept = dict(concept)
        concept.setdefault("guidelines", [])
        if self.use_pubmed:
            concept["guidelines"].append({"source":"PubMed","note":"searched last 5y (stub)"})
        concept["guidelines"].extend([
            {"source":"ADA","note":"SOC check (stub)"},
            {"source":"ACC/AHA","note":"cardio SOC (stub)"},
            {"source":"NIH/CDC","note":"labs/policy SOC (stub)"},
        ])
        return concept
