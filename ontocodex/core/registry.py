from typing import Any, Dict
_TOOLS: Dict[str, Any] = {}
def register_tool(name: str, tool: Any):
    _TOOLS[name] = tool
    return tool
def get_tool(name: str) -> Any:
    if name not in _TOOLS:
        raise KeyError(f"Tool '{name}' not registered")
    return _TOOLS[name]
def list_tools() -> Dict[str, Any]:
    return dict(_TOOLS)
