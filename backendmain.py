"""
@Author: Emily Villareal
@Version: 1.0
@Since: 10/3/2025

Usage:
    Entry point of the Tuniverse FastAPI backend.
    Initializes the app, database, routers, and background scheduler.

Change Log:
    Version 1.0 (10/3/2025): Created FastAPI app and registered routers for all modules.
"""



# main.py - FastAPI app bootstrapping
from fastapi import FastAPI
from .db import engine, Base
from .routers import users, playlists, artists, passport, compare, admin
from . import scheduler

# Create DB tables (dev)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Tuniverse Backend")

# include routers
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(playlists.router, prefix="/playlists", tags=["Playlists"])
app.include_router(artists.router, prefix="/artists", tags=["Artists"])
app.include_router(passport.router, prefix="/passport", tags=["Passport"])
app.include_router(compare.router, prefix="/compare", tags=["Comparisons"])
app.include_router(admin.router, prefix="/admin", tags=["Admin"])

# start scheduler (APScheduler)
scheduler.start_scheduler()

@app.get("/")
def root():
    return {"message": "Tuniverse backend running"}

