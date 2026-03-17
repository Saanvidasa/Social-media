from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class Comment(BaseModel):
    user_id: str
    text: str
    created_at: Optional[datetime] = None

class PostCreate(BaseModel):
    user_id: str
    content: str
    hashtags: Optional[List[str]] = []

class PostResponse(BaseModel):
    post_id: str
    user_id: str
    content: str
    hashtags: List[str]
    comments: List[Comment]
    created_at: datetime