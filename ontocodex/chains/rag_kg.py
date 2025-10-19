from typing import List, Dict, Any

class KGRAg:
    def __init__(self, retriever, llm):
        self.retriever = retriever
        self.llm = llm

    def _format(self, q: str, docs: List[str]) -> List[Dict[str, Any]]:
        ctx = "\n".join(docs[:8])
        return [
            {"role": "system", "content": "You are ontology-aware. Cite sources when present."},
            {"role": "user", "content": f"Q: {q}\nContext:\n{ctx}\nAnswer concisely with citations."},
        ]

    def invoke(self, question: str):
        docs = self.retriever.invoke(question)
        prompt = self._format(question, docs)
        return self.llm.invoke(prompt)
