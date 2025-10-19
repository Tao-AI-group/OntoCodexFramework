from pydantic import BaseModel, Field
from typing import Any, Dict, List, Optional

class Message(BaseModel):
    role: str
    content: str
    meta: Dict[str, Any] = Field(default_factory=dict)

class Document(BaseModel):
    page_content: str
    metadata: Dict[str, Any] = Field(default_factory=dict)

class ToolCall(BaseModel):
    name: str
    args: Dict[str, Any] = Field(default_factory=dict)
