from abc import ABC, abstractmethod
from ..blackboard import Blackboard
class BaseAgent(ABC):
    name: str
    def __init__(self, name: str): self.name=name
    @abstractmethod
    def step(self, bb: Blackboard) -> None: ...
