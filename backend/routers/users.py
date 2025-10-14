
"""
Backend User login, auth, & registration code
@Author: Jalen Counterman
@Version: 1.0
@Since: 10/03/2025
Usage:
Manage user registration, login, and spotify authentication
Change Log:
Version 1.0 (10/03/2025):
Created backend code for user data



# routers/users.py - registration, login, spotify oauth endpoints
from fastapi import APIRouter, Depends, HTTPException, Request, BackgroundTasks
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from .. import schemas, crud
from ..db import get_db
from ..auth import create_access_token, verify_password
from ..spotify_client import refresh_spotify_token
from typing import Dict

router = APIRouter()

@router.post("/register", response_model=schemas.UserOut)
def register(user_in: schemas.UserCreate, db: Session = Depends(get_db)):
    existing = crud.get_user_by_email(db, user_in.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    user = crud.create_user(db, user_in.email, user_in.username, user_in.password)
    return user

@router.post("/login", response_model=schemas.TokenResponse)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = crud.get_user_by_email(db, form_data.username)
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    token = create_access_token(subject=user.id)
    return {"access_token": token, "token_type": "bearer"}

# OAuth callback endpoint stub (the real flow requires redirect URIs & client secret handling)
@router.post("/spotify/callback")
def spotify_callback(payload: Dict, db: Session = Depends(get_db)):
    """
    Expect payload: {"user_id": "...", "access_token": "...", "refresh_token": "..."}
    In real app, you'd exchange code for tokens server-side.
    """
    user_id = payload.get("user_id")
    access = payload.get("access_token")
    refresh = payload.get("refresh_token")
    if not (user_id and access):
        raise HTTPException(status_code=400, detail="Missing data")
    user = crud.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    crud.set_spotify_tokens(db, user, access, refresh)
    return {"status": "ok", "user_id": user_id}

