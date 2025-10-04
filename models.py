"""
Model List Code
@Author: Emily Villareal
@Version: 1.0
@Since: 10/03/2025
Usage:
Contains all the models needed
Change Log:
Version 1.0 (10/03/2025):
Created models for code usage
"""
from sqlalchemy import Column, String, Boolean, DateTime, Integer, ForeignKey, JSON
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime
from .db import Base

class User(Base):
    __tablename__ = "users"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    password_hash = Column(String)
    spotify_linked = Column(Boolean, default=False)
    spotify_access_token = Column(String)
    spotify_refresh_token = Column(String)
    preferences = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

    playlists = relationship("Playlist", back_populates="user")

class Playlist(Base):
    __tablename__ = "playlists"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    spotify_playlist_id = Column(String)
    name = Column(String)
    track_count = Column(Integer)
    last_synced_at = Column(DateTime)

    user = relationship("User", back_populates="playlists")
    tracks = relationship("Track", back_populates="playlist")

class Track(Base):
    __tablename__ = "tracks"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    playlist_id = Column(UUID(as_uuid=True), ForeignKey("playlists.id"))
    spotify_track_id = Column(String)
    name = Column(String)
    artist_ids = Column(ARRAY(String))
    added_at = Column(DateTime)

    playlist = relationship("Playlist", back_populates="tracks")

class Artist(Base):
    __tablename__ = "artists"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    spotify_artist_id = Column(String, unique=True)
    name = Column(String)
    genres = Column(ARRAY(String))
    popularity = Column(Integer)
    origin_country = Column(String)
    origin_region = Column(String)
    confidence = Column(Integer)  # store *100
    last_checked_at = Column(DateTime)

# Add MusicPassportSummary, Comparison, ListeningHistory in the same style

