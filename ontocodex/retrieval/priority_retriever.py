from typing import Dict, Any
from ..kb.priority import PriorityRouter, KBConfig
from ..core.base import Runnable

class PriorityRetriever(Runnable):
    def __init__(self, cfg: KBConfig):
        self.router = PriorityRouter(cfg)
    def invoke(self, query: str) -> Dict[str, Any]:
        return self.router.resolve_concept(query)
