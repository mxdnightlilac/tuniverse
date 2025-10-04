"""
@Author: Tyler Tristan
@Version: 1.0
@Since: 10/03/2025

Usage:
    SQLAlchemy ORM models representing Tuniverse data schema:
    Users, Playlists, Tracks, Artists, MusicPassportSummaries, Comparisons, ListeningHistory.

Change Log:
    Version 1.0 (10/3/2025): Created models aligned with PVD data definitions.
"""



# models.py - ORM models matching your pseudo-code
import uuid
from sqlalchemy import Column, String, Boolean, DateTime, Integer, ForeignKey, JSON, Table, Text
from sqlalchemy.dialects.postgresql import UUID as PG_UUID, ARRAY
from sqlalchemy.orm import relationship
from datetime import datetime
from .db import Base

# Use simple text columns; ARRAY/Postgres-specific types can be swapped in real DB.
class User(Base):
    __tablename__ = "users"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=True)
    spotify_linked = Column(Boolean, default=False)
    spotify_access_token = Column(Text, nullable=True)
    spotify_refresh_token = Column(Text, nullable=True)
    preferences = Column(JSON, default={})
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

    playlists = relationship("Playlist", back_populates="user")
    passports = relationship("MusicPassportSummary", back_populates="user")

class Playlist(Base):
    __tablename__ = "playlists"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"))
    spotify_playlist_id = Column(String, index=True)
    name = Column(String)
    track_count = Column(Integer, default=0)
    last_synced_at = Column(DateTime, nullable=True)

    user = relationship("User", back_populates="playlists")
    tracks = relationship("Track", back_populates="playlist")

class Track(Base):
    __tablename__ = "tracks"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    playlist_id = Column(String, ForeignKey("playlists.id"))
    spotify_track_id = Column(String, index=True)
    name = Column(String)
    artist_ids = Column(JSON, default=[])
    added_at = Column(DateTime, nullable=True)

    playlist = relationship("Playlist", back_populates="tracks")

class Artist(Base):
    __tablename__ = "artists"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    spotify_artist_id = Column(String, unique=True, index=True)
    name = Column(String)
    genres = Column(JSON, default=[])
    popularity = Column(Integer, nullable=True)
    origin_country = Column(String, nullable=True)
    origin_region = Column(String, nullable=True)
    coordinates = Column(JSON, nullable=True)  # {"lat":..,"lon":..}
    confidence = Column(Integer, default=0)  # 0-100
    last_checked_at = Column(DateTime, nullable=True)

class MusicPassportSummary(Base):
    __tablename__ = "music_passport_summaries"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    country_counts = Column(JSON, default={})
    region_percentages = Column(JSON, default={})
    total_artists = Column(Integer, default=0)

    user = relationship("User", back_populates="passports")

class Comparison(Base):
    __tablename__ = "comparisons"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, nullable=False)
    friend_ids = Column(JSON, default=[])
    created_at = Column(DateTime, default=datetime.utcnow)
    results = Column(JSON, default={})

class ListeningHistory(Base):
    __tablename__ = "listening_history"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, index=True)
    track_id = Column(String)
    track_name = Column(String)
    artist_id = Column(String)
    played_at = Column(DateTime, nullable=True)

