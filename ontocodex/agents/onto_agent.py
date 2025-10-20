from typing import Dict, Any
from ..retrieval.priority_retriever import PriorityRetriever
from ..chains.evidence import EvidenceEnforcer
from ..mapping.tools import MappingTool, MappingArgs
from ..core.memory import ConversationMemory
from .planner_llm import TinyPlanner
class OntoCodexAgent:
    def __init__(self, retriever: PriorityRetriever, enforcer: EvidenceEnforcer, mapper: MappingTool, memory: ConversationMemory, data_dir: str = 'data'):
        self.retriever=retriever; self.enforcer=enforcer; self.mapper=mapper; self.memory=memory; self.data_dir=data_dir; self.planner=TinyPlanner(memory)
    def invoke(self, user_text: str) -> Dict[str, Any]:
        self.memory.add('user', user_text); plan=self.planner.plan(user_text)
        if plan['action']=='MAP':
            term=user_text; table=plan['table'] or self.memory.get_slot('last_table','rxnorm')
            mapped=self.mapper.invoke(MappingArgs(term=term, table=table, data_dir=self.data_dir))
            out={'plan':plan,'result':mapped}
        else:
            concept=self.retriever.invoke(user_text); ev=[]
            if concept.get('definition'): ev.append({'text':concept['definition'],'source':concept.get('source',''),'path':'definition'})
            concept['evidence']=ev; concept=self.enforcer.invoke(concept); out={'plan':plan,'result':concept}
        self.memory.add('agent', out); 
        if plan.get('table'): self.memory.set_slot('last_table', plan['table'])
        return out
