from .base_agent import BaseAgent
from ..blackboard import Blackboard
from ...kb.priority import KBConfig
from ...retrieval.priority_retriever import PriorityRetriever
class RetrieverAgent(BaseAgent):
    def __init__(self, cfg: KBConfig, name: str = 'retriever'):
        super().__init__(name); self.retriever=PriorityRetriever(cfg)
    def step(self, bb: Blackboard) -> None:
        for msg in bb.query(receiver=self.name, type='task'):
            if msg.content.get('task')!='phenotype': continue
            term=msg.content.get('term'); 
            if not term: continue
            concept=self.retriever.invoke(term)
            if concept.get('definition'):
                concept['evidence']=[{'text':concept['definition'],'source':concept.get('source',''),'path':'definition'}]
            bb.post(sender=self.name, receiver='coordinator', type='result', content={'task':'phenotype','term':term,'concept':concept})
