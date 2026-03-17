from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UserCreate(BaseModel):
    username: str
    email: str
    bio: Optional[str] = ""

class UserResponse(BaseModel):
    user_id: str
    username: str
    email: str
    bio: str
    created_at: datetime