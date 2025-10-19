from typing import Any, Dict
class Provenance:
    def __init__(self):
        self.events = []
    def log(self, kind: str, payload: Dict[str, Any]):
        self.events.append({"kind": kind, "payload": payload})
    def dump(self):
        return self.events
