from typing import Any, Dict, List
from dataclasses import dataclass, field
import time
@dataclass
class Turn: role: str; content: Any; timestamp: float = field(default_factory=lambda: time.time())
class ConversationMemory:
    def __init__(self, max_turns: int = 50): self.turns: List[Turn] = []; self.max_turns=max_turns; self.slots: Dict[str,Any]={}
    def add(self, role: str, content: Any): self.turns.append(Turn(role,content)); 
    def get_history(self, last_n: int = 10) -> List[Turn]: return self.turns[-last_n:]
    def to_prompt(self, last_n: int = 6) -> str: return "\n".join([f"{t.role.upper()}: {t.content}" for t in self.get_history(last_n)])
    def set_slot(self, k: str, v: Any): self.slots[k]=v
    def get_slot(self, k: str, default=None): return self.slots.get(k, default)
