"""
@Author: Tyler Tristan
@Version: 1.0
@Since: 10/03/2025

Usage:
    Manages artist metadata enrichment from Spotify and MusicBrainz APIs.

Change Log:
    Version 1.0 (10/03/2025): Implemented artist enrichment and artist listing endpoints.
"""



# routers/artists.py - enrichment & artist endpoints
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from ..db import get_db
from .. import crud, spotify_client, utils
from .. import models

router = APIRouter()

@router.post("/enrich/{user_id}")
def enrich_artists(user_id: str, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    """
    Enrich all artists referenced by a user's playlists.
    """
    background_tasks.add_task(_enrich_worker, user_id)
    return {"status": "enrich scheduled"}

def _enrich_worker(user_id: str):
    db = next(get_db())
    # find unique artist IDs from tracks
    artist_ids = set()
    tracks = db.query(models.Track).join(models.Playlist).filter(models.Playlist.user_id == user_id).all()
    for t in tracks:
        for aid in (t.artist_ids or []):
            artist_ids.add(aid)
    user = db.query(models.User).filter(models.User.id == user_id).first()
    token = user.spotify_access_token if user else None
    for aid in artist_ids:
        # get from spotify
        aresp = spotify_client.spotify_get(f"/artists/{aid}", token)
        if not aresp or "error" in aresp:
            # fallback to MusicBrainz by name (if we had name)
            continue
        name = aresp.get("name")
        genres = aresp.get("genres", [])
        popularity = aresp.get("popularity")
        origin_country = aresp.get("country")  # spotify often doesn't include
        # fallback:
        if not origin_country:
            mb = utils.musicbrainz_lookup_artist(name)
            if mb:
                origin_country = mb.get("country")
                coords = {"lat": mb.get("lat"), "lon": mb.get("lon")} if mb.get("lat") else None
                confidence = 80
            else:
                coords = None
                confidence = 20
        else:
            coords = utils.geocode_country(origin_country)
            confidence = 90
        crud.upsert_artist(db, aid, name, genres=genres, popularity=popularity, origin_country=origin_country, coordinates=coords, confidence=confidence)
    db.close()

@router.get("/for_user/{user_id}")
def list_user_artists(user_id: str, db: Session = Depends(get_db)):
    # return artist list mapped to user's tracks
    tracks = db.query(models.Track).join(models.Playlist).filter(models.Playlist.user_id == user_id).all()
    artist_ids = set()
    for t in tracks:
        for a in (t.artist_ids or []):
            artist_ids.add(a)
    artists = db.query(models.Artist).filter(models.Artist.spotify_artist_id.in_(list(artist_ids))).all() if artist_ids else []
    return [{"spotify_artist_id": a.spotify_artist_id, "name": a.name, "origin_country": a.origin_country, "coordinates": a.coordinates, "confidence": a.confidence} for a in artists]

