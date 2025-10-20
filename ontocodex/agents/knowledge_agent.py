from typing import Dict, Any, List
try:
    from ..guidelines.tool import GuidelineTool
except Exception:
    GuidelineTool = None

class KnowledgebaseAgent:
    def __init__(self, memory):
        self.memory = memory
        self.guidelines = GuidelineTool() if GuidelineTool else None

    def gather(self, query: str) -> Dict[str, Any]:
        results: List[Dict[str, Any]] = []
        entities: List[str] = []
        if self.guidelines:
            try:
                results = self.guidelines.invoke(query)
            except Exception as e:
                results = [{"error": str(e)}]
        for r in results:
            t = r.get("title","")
            if t:
                entities.append(t.split(":")[0][:64])
        return {"evidence": results, "entities": entities}
