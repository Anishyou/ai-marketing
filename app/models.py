from pydantic import BaseModel
from typing import List, Optional

class ChatRequest(BaseModel):
    prompt: str

class PostContent(BaseModel):
    caption: str
    image_prompt: str
    image_url: str

class ChatResponse(BaseModel):
    strategy: str
    posts: List[PostContent]
    detected_url: Optional[str] = None
    detected_timeframe: Optional[str] = None
