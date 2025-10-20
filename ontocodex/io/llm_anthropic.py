from typing import List, Dict, Any
import anthropic
class AnthropicPlannerLLM:
    def __init__(self, model:str='claude-3-5-sonnet-20240620', temperature:float=0.2): self.client=anthropic.Anthropic(); self.model=model; self.temperature=temperature
    def invoke(self, messages:List[Dict[str,Any]])->Dict[str,Any]:
        sys=next((m['content'] for m in messages if m['role']=='system'), '')
        usr='\n'.join([m['content'] for m in messages if m['role']=='user'])
        resp=self.client.messages.create(model=self.model, system=sys, messages=[{'role':'user','content':usr}], max_tokens=100, temperature=self.temperature)
        return {'role':'assistant','content': resp.content[0].text.strip()}
