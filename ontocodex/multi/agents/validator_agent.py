from .base_agent import BaseAgent
from ..blackboard import Blackboard
class ValidatorAgent(BaseAgent):
    def __init__(self, name: str = 'validator'): super().__init__(name)
    def step(self, bb: Blackboard) -> None:
        last=bb.latest(receiver='coordinator', type='result')
        if not last: return
        c=last.content
        if c.get('task')=='phenotype':
            concept=c.get('concept',{}); ev=concept.get('evidence',[]); concept['status']='ACCEPTED' if ev else 'REJECTED_NO_EVIDENCE'
            bb.post(sender=self.name, receiver='coordinator', type='result', content={'task':'validation','term':c.get('term'),'status':concept['status']})
