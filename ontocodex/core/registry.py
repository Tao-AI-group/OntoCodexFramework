from typing import Any, Dict
_TOOLS: Dict[str, Any]={}
def register_tool(n:str,t:Any): _TOOLS[n]=t; return t
def get_tool(n:str)->Any: 
    if n not in _TOOLS: raise KeyError(f"Tool '{n}' not registered"); return _TOOLS[n]
def list_tools()->Dict[str,Any]: return dict(_TOOLS)
