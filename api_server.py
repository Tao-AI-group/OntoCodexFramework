from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, Optional
import os
import uuid

# OntoCodex imports (install your framework separately)
from ontocodex.kb.priority import KBConfig
from ontocodex.retrieval.priority_retriever import PriorityRetriever
from ontocodex.chains.evidence import EvidenceEnforcer
from ontocodex.mapping.tools import MappingTool
from ontocodex.core.memory import ConversationMemory
from ontocodex.agents.onto_agent import OntoCodexAgent

APP_TITLE = "OntoCodex Chat API"
APP_VERSION = "0.8.0"

DATA_DIR = os.environ.get("ONTOCODEX_DATA_DIR", "data")

# -------- Session store (in-memory) --------
class SessionState:
    def __init__(self, agent: OntoCodexAgent, memory: ConversationMemory):
        self.agent = agent
        self.memory = memory

SESSIONS: Dict[str, SessionState] = {}

def _new_agent() -> SessionState:
    cfg = KBConfig(
        doid_path=os.path.join(DATA_DIR, "DOID.owl"),
        medlineplus_path=os.path.join(DATA_DIR, "MEDLINEPLUS.ttl"),
        hp_path=os.path.join(DATA_DIR, "HP.csv"),
    )
    memory = ConversationMemory(max_turns=50)
    agent = OntoCodexAgent(
        retriever=PriorityRetriever(cfg),
        enforcer=EvidenceEnforcer(strict=True),
        mapper=MappingTool(),
        memory=memory,
        data_dir=DATA_DIR,
    )
    return SessionState(agent=agent, memory=memory)

def get_or_create_session(session_id: Optional[str]) -> str:
    if session_id and session_id in SESSIONS:
        return session_id
    sid = session_id or str(uuid.uuid4())
    SESSIONS[sid] = _new_agent()
    return sid

# -------- FastAPI app --------
app = FastAPI(title=APP_TITLE, version=APP_VERSION, docs_url="/docs", redoc_url=None)

class ChatRequest(BaseModel):
    session_id: Optional[str] = None
    user_text: str

class ChatResponse(BaseModel):
    session_id: str
    plan: Dict[str, Any]
    result: Dict[str, Any]
    memory_last: list

class ResetRequest(BaseModel):
    session_id: str

@app.get("/ping")
def ping():
    return {"ok": True, "message": f"{APP_TITLE} v{APP_VERSION}", "data_dir": DATA_DIR}

@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    sid = get_or_create_session(req.session_id)
    st = SESSIONS[sid]
    out = st.agent.invoke(req.user_text)
    # Prepare response; `out` contains {"plan":..., "result":...}
    plan = out.get("plan", {"action": "unknown"})
    result = out.get("result", {})
    mem = [ {"role": t.role, "content": t.content} for t in st.memory.get_history(8) ]
    return ChatResponse(session_id=sid, plan=plan, result=result, memory_last=mem)

@app.post("/reset")
def reset(req: ResetRequest):
    if req.session_id in SESSIONS:
        SESSIONS[req.session_id] = _new_agent()
        return {"ok": True, "message": "Session reset", "session_id": req.session_id}
    raise HTTPException(status_code=404, detail="Unknown session_id")

@app.get("/session/{session_id}/history")
def history(session_id: str):
    if session_id not in SESSIONS:
        raise HTTPException(status_code=404, detail="Unknown session_id")
    st = SESSIONS[session_id]
    return {
        "session_id": session_id,
        "history": [ {"role": t.role, "content": t.content} for t in st.memory.get_history(50) ]
    }

@app.get("/config")
def config():
    # Try to expose planner backend class name if available
    meta = {"data_dir": DATA_DIR}
    try:
        # Peek at any existing session
        if SESSIONS:
            sample = next(iter(SESSIONS.values()))
            meta["planner_impl"] = sample.agent.planner.llm.__class__.__name__
        else:
            # bootstrap a temp agent to introspect
            temp = _new_agent()
            meta["planner_impl"] = temp.agent.planner.llm.__class__.__name__
    except Exception as e:
        meta["planner_impl"] = f"unknown ({e})"
    return meta
