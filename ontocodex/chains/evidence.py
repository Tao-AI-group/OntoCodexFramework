from typing import Dict, Any, List
from dataclasses import dataclass
from ..core.base import Runnable
@dataclass
class EvidenceItem: text:str; source:str; path:str
class EvidenceEnforcer(Runnable):
    def __init__(self, strict: bool = True): self.strict=strict
    def invoke(self, cand: Dict[str,Any]) -> Dict[str,Any]:
        ev: List[EvidenceItem] = cand.get('evidence', [])
        cand['status'] = 'ACCEPTED' if (ev or not self.strict) else 'REJECTED_NO_EVIDENCE'
        return cand
