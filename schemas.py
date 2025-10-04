from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime
import uuid

class UserCreate(BaseModel):
    email: EmailStr
    username: str
    password: str

class UserOut(BaseModel):
    id: uuid.UUID
    email: str
    username: str
    spotify_linked: bool
    created_at: datetime

    class Config:
        orm_mode = True

class PlaylistOut(BaseModel):
    id: uuid.UUID
    name: str
    track_count: int
    last_synced_at: Optional[datetime]
