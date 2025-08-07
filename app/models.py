from pydantic import BaseModel, HttpUrl
from typing import List, Optional

class ChatRequest(BaseModel):
    project_name: str
    website_url: HttpUrl
    description: Optional[str] = None
    goals: List[str]  # e.g. ["Awareness", "Sales"]
    timeframe: Optional[str] = None  # e.g. "next week"

class PostContent(BaseModel):
    caption: str
    image_prompt: str
    image_url: str

class ChatResponse(BaseModel):
    strategy: str
    posts: List[PostContent]
    detected_url: Optional[str] = None
    detected_timeframe: Optional[str] = None
