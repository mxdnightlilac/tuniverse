"""
@Author: Max Henson
@Version: 1.0
@Since: 10/3/2025

Usage:
    Handles database engine, session, and base model setup using SQLAlchemy. 
    Provides dependency injection for DB sessions.

Change Log:
    Version 1.0 (10/3/2025): Initial creation
"""




# db.py - SQLAlchemy engine + session + Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./tuniverse.db")

# For SQLite (dev). In production use PostgreSQL or similar.
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

