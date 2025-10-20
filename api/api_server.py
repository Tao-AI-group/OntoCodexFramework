from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, Optional
import os, uuid
from ontocodex.kb.priority import KBConfig
from ontocodex.retrieval.priority_retriever import PriorityRetriever
from ontocodex.chains.evidence import EvidenceEnforcer
from ontocodex.mapping.tools import MappingTool
from ontocodex.core.memory import ConversationMemory
from ontocodex.agents.onto_agent import OntoCodexAgent
from ontocodex.multi.agents.retriever_agent import RetrieverAgent
from ontocodex.multi.agents.mapper_agent import MapperAgent
from ontocodex.multi.agents.guideline_agent import GuidelineAgent
from ontocodex.multi.agents.validator_agent import ValidatorAgent
from ontocodex.multi.orchestrator_planned import CodexOrchestratorPlanned
APP_TITLE='OntoCodex API'; APP_VERSION='1.1.0'; DATA_DIR=os.environ.get('ONTOCODEX_DATA_DIR','data')
class SessionState:
    def __init__(self, agent: OntoCodexAgent, memory: ConversationMemory, orchestrator: CodexOrchestratorPlanned): self.agent=agent; self.memory=memory; self.orchestrator=orchestrator
SESSIONS: Dict[str, SessionState]={}
def _new_state()->SessionState:
    cfg=KBConfig(doid_path=os.path.join(DATA_DIR,'DOID.owl'), medlineplus_path=os.path.join(DATA_DIR,'MEDLINEPLUS.ttl'), hp_path=os.path.join(DATA_DIR,'HP.csv'))
    memory=ConversationMemory(50); single=OntoCodexAgent(PriorityRetriever(cfg), EvidenceEnforcer(True), MappingTool(), memory, data_dir=DATA_DIR)
    ma=[RetrieverAgent(cfg), MapperAgent(data_dir=DATA_DIR), GuidelineAgent(), ValidatorAgent()]; orch=CodexOrchestratorPlanned(ma, memory=memory)
    return SessionState(single, memory, orch)
def get_or_create(sid: Optional[str])->str:
    if sid and sid in SESSIONS: return sid
    ns=sid or str(uuid.uuid4()); SESSIONS[ns]=_new_state(); return ns
app=FastAPI(title=APP_TITLE, version=APP_VERSION, docs_url='/docs', redoc_url=None)
class ChatReq(BaseModel): session_id: Optional[str]=None; user_text: str
class ChatRes(BaseModel): session_id: str; plan: Dict[str,Any]; result: Dict[str,Any]; memory_last: list
class ChatMARes(BaseModel): session_id: str; plan: Dict[str,Any]; results: list; memory_last: list
@app.get('/ping')
def ping(): return {'ok':True,'message':f'{APP_TITLE} v{APP_VERSION}','data_dir':DATA_DIR}
@app.post('/chat', response_model=ChatRes)
def chat(req: ChatReq):
    sid=get_or_create(req.session_id); st=SESSIONS[sid]; out=st.agent.invoke(req.user_text); plan=out.get('plan',{}); result=out.get('result',{})
    mem=[{'role':t.role,'content':t.content} for t in st.memory.get_history(8)]; return ChatRes(session_id=sid, plan=plan, result=result, memory_last=mem)
@app.post('/chat_ma', response_model=ChatMARes)
def chat_ma(req: ChatReq):
    sid=get_or_create(req.session_id); st=SESSIONS[sid]; out=st.orchestrator.chat_turn(req.user_text, max_rounds=4); plan=out.get('plan',{}); results=out.get('results',[])
    mem=[{'role':t.role,'content':t.content} for t in st.memory.get_history(8)]; return ChatMARes(session_id=sid, plan=plan, results=results, memory_last=mem)
