"""
@Author: Max Henson
@Version: 1.0
@Since: 10/3/2025

Usage:
    Admin-only endpoints for system metrics and user data purging.

Change Log:
    Version 1.0 (10/3/2025): Implemented /status and /user/{id} delete routes.
"""



# routers/admin.py - admin utilities
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..db import get_db
from .. import models
import os
from typing import Dict

router = APIRouter()

@router.get("/status")
def system_status(db: Session = Depends(get_db)):
    user_count = db.query(models.User).count()
    artist_count = db.query(models.Artist).count()
    playlist_count = db.query(models.Playlist).count()
    return {"users": user_count, "artists": artist_count, "playlists": playlist_count}

@router.delete("/user/{user_id}")
def purge_user(user_id: str, db: Session = Depends(get_db)):
    # caution: deletes data; permission checks omitted in skeleton
    db.query(models.ListeningHistory).filter(models.ListeningHistory.user_id == user_id).delete()
    db.query(models.Playlist).filter(models.Playlist.user_id == user_id).delete()
    db.query(models.MusicPassportSummary).filter(models.MusicPassportSummary.user_id == user_id).delete()
    db.query(models.User).filter(models.User.id == user_id).delete()
    db.commit()
    return {"status": "deleted", "user_id": user_id}

