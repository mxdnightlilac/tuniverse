"""
Backend User Data Logic
@Author: Jalen Counterman
@Version: 1.0
@Since: 10/03/2025
Usage:
Control data displayed specific to the user
Change Log:
Version 1.0 (10/03/2025):
Created backend code for user data
"""
# schemas.py - pydantic models for requests/responses
from pydantic import BaseModel, EmailStr
from typing import List, Optional, Dict, Any
from datetime import datetime

class UserCreate(BaseModel):
    email: EmailStr
    username: str
    password: str

class UserOut(BaseModel):
    id: str
    email: str
    username: str
    spotify_linked: bool
    created_at: datetime

    class Config:
        orm_mode = True

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

class PlaylistOut(BaseModel):
    id: str
    spotify_playlist_id: str
    name: str
    track_count: int
    last_synced_at: Optional[datetime]

    class Config:
        orm_mode = True

class ArtistOut(BaseModel):
    spotify_artist_id: str
    name: str
    origin_country: Optional[str]
    origin_region: Optional[str]
    coordinates: Optional[Dict[str, float]]
    confidence: int

class PassportSummaryOut(BaseModel):
    id: str
    user_id: str
    created_at: datetime
    country_counts: Dict[str, int]
    region_percentages: Dict[str, float]
    total_artists: int

    class Config:
        orm_mode = True


