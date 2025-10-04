# crud.py - basic DB operations used by routers
from sqlalchemy.orm import Session
from . import models
from .auth import hash_password
from datetime import datetime

def create_user(db: Session, email: str, username: str, password: str):
    hashed = hash_password(password)
    user = models.User(email=email, username=username, password_hash=hashed)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_user(db: Session, user_id: str):
    return db.query(models.User).filter(models.User.id == user_id).first()

def set_spotify_tokens(db: Session, user: models.User, access_token: str, refresh_token: str):
    user.spotify_access_token = access_token
    user.spotify_refresh_token = refresh_token
    user.spotify_linked = True
    user.updated_at = datetime.utcnow()
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def create_playlist(db: Session, user_id: str, spotify_playlist_id: str, name: str, track_count: int):
    pl = models.Playlist(user_id=user_id, spotify_playlist_id=spotify_playlist_id, name=name, track_count=track_count)
    db.add(pl)
    db.commit()
    db.refresh(pl)
    return pl

def upsert_artist(db: Session, spotify_artist_id: str, name: str, **kwargs):
    existing = db.query(models.Artist).filter(models.Artist.spotify_artist_id == spotify_artist_id).first()
    if existing:
        for k, v in kwargs.items():
            setattr(existing, k, v)
        db.add(existing)
        db.commit()
        db.refresh(existing)
        return existing
    a = models.Artist(spotify_artist_id=spotify_artist_id, name=name, **kwargs)
    db.add(a)
    db.commit()
    db.refresh(a)
    return a

def create_passport(db: Session, user_id: str, country_counts: dict, region_percentages: dict, total_artists: int):
    p = models.MusicPassportSummary(user_id=user_id, country_counts=country_counts, region_percentages=region_percentages, total_artists=total_artists)
    db.add(p)
    db.commit()
    db.refresh(p)
    return p
