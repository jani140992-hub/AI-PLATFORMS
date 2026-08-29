from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

class ChatMessageParam(BaseModel):
    role: str
    content: str
    name: Optional[str] = None

class ChatChoice(BaseModel):
    index: int
    message: ChatMessageParam
    finish_reason: Optional[str] = None

class Usage(BaseModel):
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int

class ChatCompletion(BaseModel):
    id: str
    created: int
    model: str
    choices: List[ChatChoice]
    usage: Usage

class ChatStreamChunk(BaseModel):
    id: str
    delta: str
    finish_reason: Optional[str] = None
