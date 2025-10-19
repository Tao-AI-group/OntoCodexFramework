from typing import List, Dict, Any
try:
    from openai import OpenAI
except Exception:
    OpenAI = None  # optional

class ChatOpenAI:
    def __init__(self, model: str = "gpt-4o-mini", api_key: str | None = None):
        self.model = model
        self.api_key = api_key
        self.client = OpenAI(api_key=api_key) if (OpenAI and api_key) else None

    def invoke(self, messages: List[Dict[str, Any]]):
        if not self.client:
            # Fallback stub for offline runs
            joined = "\n".join([m.get("content","") for m in messages])
            return {"role":"assistant","content": f"[STUB LLM] {joined[:200]}..."}
        resp = self.client.chat.completions.create(model=self.model, messages=messages)
        return {"role":"assistant","content": resp.choices[0].message.content}
