from abc import ABC, abstractmethod
from typing import Any
from ..blackboard import Blackboard

class BaseAgent(ABC):
    name: str
    def __init__(self, name: str):
        self.name = name
    @abstractmethod
    def step(self, bb: Blackboard) -> None:
        """Consume messages for me and optionally post new messages."""
        ...

    # Helper for safe dict gets
    def _get(self, d: dict, key: str, default=None):
        return d[key] if key in d else default
