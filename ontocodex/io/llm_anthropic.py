from typing import List, Dict, Any
import anthropic

class AnthropicPlannerLLM:
    """
    Uses Anthropic Claude for planning; requires ANTHROPIC_API_KEY.
    """
    def __init__(self, model: str = "claude-3-5-sonnet-20240620", temperature: float = 0.2):
        self.client = anthropic.Anthropic()
        self.model = model
        self.temperature = temperature

    def invoke(self, messages: List[Dict[str, Any]]) -> Dict[str, Any]:
        system_prompt = next((m["content"] for m in messages if m["role"] == "system"), "")
        user_input = "\n".join([m["content"] for m in messages if m["role"] == "user"])
        resp = self.client.messages.create(
            model=self.model,
            system=system_prompt,
            messages=[{"role": "user", "content": user_input}],
            max_tokens=100,
            temperature=self.temperature,
        )
        return {"role": "assistant", "content": resp.content[0].text.strip()}
