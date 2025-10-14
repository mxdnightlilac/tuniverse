"""
Backend Passport Coding
@Author: Tyler Tristan
@Version: 1.0
@Since: 10/03/2025
Usage:
Generate the user's customized music passport
Change Log:
Version 1.0 (10/03/2025):
Created backend code for the music passport
"""



# routers/passport.py - generate music passport summary + image stub
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..db import get_db
from .. import crud, models
from ..schemas import PassportSummaryOut
from typing import Dict
import json
import os

router = APIRouter()

@router.get("/{user_id}", response_model=PassportSummaryOut)
def get_passport(user_id: str, db: Session = Depends(get_db)):
    """
    Generate (or fetch latest) music passport summary for user.
    """
    # Simple: compute on-demand
    # Gather artists for user
    tracks = db.query(models.Track).join(models.Playlist).filter(models.Playlist.user_id == user_id).all()
    artist_ids = set()
    for t in tracks:
        for aid in (t.artist_ids or []):
            artist_ids.add(aid)
    artists = db.query(models.Artist).filter(models.Artist.spotify_artist_id.in_(list(artist_ids))).all() if artist_ids else []
    country_counts: Dict[str, int] = {}
    for a in artists:
        c = a.origin_country or "Unknown"
        country_counts[c] = country_counts.get(c, 0) + 1
    total = len(artists)
    region_percentages = {}  # stub: region mapping
    for k, v in country_counts.items():
        region_percentages[k] = (v / total * 100) if total else 0.0
    passport = crud.create_passport(db, user_id, country_counts, region_percentages, total)
    # image generation stub (store path)
    image_path = os.path.join("share_images", f"passport_{passport.id}.png")
    # In real implementation: call render_passport_image()
    return passport

