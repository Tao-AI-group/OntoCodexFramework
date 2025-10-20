from typing import List, Dict, Any
from openai import OpenAI
class OpenAIPlannerLLM:
    def __init__(self, model:str='gpt-4o-mini', temperature:float=0.2): self.client=OpenAI(); self.model=model; self.temperature=temperature
    def invoke(self, messages:List[Dict[str,Any]])->Dict[str,Any]:
        r=self.client.chat.completions.create(model=self.model, messages=messages, temperature=self.temperature, max_tokens=100)
        return {'role':'assistant','content': r.choices[0].message.content.strip()}
