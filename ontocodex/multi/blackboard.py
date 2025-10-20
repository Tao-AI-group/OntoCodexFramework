from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
import time, uuid
@dataclass
class Message: id:str; sender:str; receiver:str; type:str; content:Dict[str,Any]; ts:float=field(default_factory=lambda: time.time())
def _id(): return str(uuid.uuid4())
class Blackboard:
    def __init__(self): self.messages:List[Message]=[]; self.kv:Dict[str,Any]={}
    def post(self,sender:str,receiver:str,type:str,content:Dict[str,Any])->Message:
        m=Message(id=_id(),sender=sender,receiver=receiver,type=type,content=content); self.messages.append(m); return m
    def query(self, receiver: Optional[str]=None, type: Optional[str]=None) -> List[Message]:
        out=self.messages
        if receiver: out=[m for m in out if m.receiver in (receiver,'broadcast')]
        if type: out=[m for m in out if m.type==type]
        return out
    def latest(self, receiver: Optional[str]=None, type: Optional[str]=None):
        q=self.query(receiver,type); return q[-1] if q else None
    def set(self,k:str,v:Any): self.kv[k]=v
    def get(self,k:str,default=None): return self.kv.get(k, default)
