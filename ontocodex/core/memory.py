from typing import Any, Dict, List, Optional
from dataclasses import dataclass, field
import time

@dataclass
class Turn:
    role: str  # "user" | "agent" | "tool"
    content: Any
    timestamp: float = field(default_factory=lambda: time.time())

class ConversationMemory:
    """Simple in-memory conversation store with metadata."""
    def __init__(self, max_turns: int = 50):
        self.turns: List[Turn] = []
        self.max_turns = max_turns
        self.slots: Dict[str, Any] = {}  # scratchpad for extracted entities

    def add(self, role: str, content: Any):
        self.turns.append(Turn(role=role, content=content))
        if len(self.turns) > self.max_turns:
            self.turns = self.turns[-self.max_turns:]

    def get_history(self, last_n: int = 10) -> List[Turn]:
        return self.turns[-last_n:]

    def set_slot(self, key: str, value: Any):
        self.slots[key] = value

    def get_slot(self, key: str, default=None):
        return self.slots.get(key, default)

    def to_prompt(self, last_n: int = 6) -> str:
        lines = []
        for t in self.get_history(last_n):
            lines.append(f"{t.role.upper()}: {t.content}")
        return "\n".join(lines)
