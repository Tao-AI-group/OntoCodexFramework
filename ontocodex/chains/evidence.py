from typing import Dict, Any, List
from dataclasses import dataclass

@dataclass
class EvidenceItem:
    text: str
    source: str
    path: str

class EvidenceEnforcer:
    def __init__(self, strict: bool = True):
        self.strict = strict
    def enforce(self, candidate: Dict[str, Any]) -> Dict[str, Any]:
        evidence: List[EvidenceItem] = candidate.get("evidence", [])
        if not evidence and self.strict:
            candidate["status"] = "REJECTED_NO_EVIDENCE"
            return candidate
        candidate["status"] = "ACCEPTED"
        return candidate
