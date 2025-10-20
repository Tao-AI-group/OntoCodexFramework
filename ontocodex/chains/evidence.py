from typing import Dict, Any, List
from dataclasses import dataclass
from ..core.base import Runnable

@dataclass
class EvidenceItem:
    text: str
    source: str
    path: str

class EvidenceEnforcer(Runnable):
    def __init__(self, strict: bool = True):
        self.strict = strict
    def invoke(self, candidate: Dict[str, Any]) -> Dict[str, Any]:
        evidence: List[EvidenceItem] = candidate.get("evidence", [])
        if not evidence and self.strict:
            candidate["status"] = "REJECTED_NO_EVIDENCE"
        else:
            candidate["status"] = "ACCEPTED"
        return candidate
