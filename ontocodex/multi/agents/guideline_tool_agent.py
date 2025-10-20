from .base_agent import BaseAgent
from ..blackboard import Blackboard
from ...guidelines.tool import GuidelineTool

class GuidelineToolAgent(BaseAgent):
    """Agent wrapping GuidelineTool (PubMed-based)."""
    def __init__(self, name: str = "guideline_tool"):
        super().__init__(name)
        self.tool = GuidelineTool()

    def step(self, bb: Blackboard) -> None:
        for msg in bb.query(receiver=self.name, type="task"):
            if msg.content.get("task") != "guidelines":
                continue
            term = msg.content.get("term", "")
            results = self.tool.invoke(term)
            bb.post(sender=self.name, receiver="coordinator", type="result",
                    content={"task":"guidelines","term":term,"guidelines":results})
