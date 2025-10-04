"""
Playlist & Listening History Coding
@Author: Tyler Tristan
@Version: 1.0
@Since: 10/03/2025
Usage:
Import playlist data and listening history
Change Log:
Version 1.0 (10/03/2025):
Created backend code for the playlist history
"""
# routers/playlists.py - import & sync playlists, import listening history
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from ..db import get_db
from .. import crud, spotify_client
from .. import models
from typing import List, Dict

router = APIRouter()

@router.post("/sync/{user_id}")
def sync_playlists(user_id: str, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    """
    Start background sync of playlists and tracks for this user.
    """
    user = crud.get_user(db, user_id)
    if not user or not user.spotify_linked:
        raise HTTPException(status_code=400, detail="Spotify not linked for user")
    background_tasks.add_task(_background_sync, user_id)
    return {"status": "sync scheduled"}

def _background_sync(user_id: str):
    """
    Background worker: fetch playlists via Spotify API, store in DB.
    """
    db = next(get_db())
    user = crud.get_user(db, user_id)
    if not user:
        return
    token = user.spotify_access_token
    playlists_resp = spotify_client.spotify_get("/me/playlists", token, params={"limit": 50})
    if not playlists_resp or "error" in playlists_resp:
        return
    for item in playlists_resp.get("items", []):
        pid = item.get("id")
        name = item.get("name")
        total = item.get("tracks", {}).get("total", 0)
        pl = crud.create_playlist(db, user_id, pid, name, total)
        # naive tracks fetch (pagination omitted)
        tracks_resp = spotify_client.spotify_get(f"/playlists/{pid}/tracks", token, params={"limit": 50})
        for t in tracks_resp.get("items", []):
            track = t.get("track")
            if not track:
                continue
            # create track rows (simplified)
            tr = models.Track(playlist_id=pl.id, spotify_track_id=track.get("id"), name=track.get("name"), artist_ids=[a.get("id") for a in track.get("artists", [])])
            db.add(tr)
    db.commit()
    db.close()

@router.post("/history/import/{user_id}")
def import_listening_history(user_id: str, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    user = crud.get_user(db, user_id)
    if not user or not user.spotify_linked:
        raise HTTPException(status_code=400, detail="Spotify not linked")
    background_tasks.add_task(_import_history, user_id)
    return {"status": "history import scheduled"}

def _import_history(user_id: str):
    db = next(get_db())
    user = crud.get_user(db, user_id)
    token = user.spotify_access_token
    url = "/me/player/recently-played?limit=50"
    # naive pagination
    resp = spotify_client.spotify_get(url, token)
    if not resp:
        return
    for item in resp.get("items", []):
        track = item.get("track")
        played_at = item.get("played_at")
        if not track:
            continue
        lh = models.ListeningHistory(user_id=user_id, track_id=track.get("id"), track_name=track.get("name"), artist_id=track.get("artists", [{}])[0].get("id"), played_at=played_at)
        db.add(lh)
    db.commit()
    db.close()


