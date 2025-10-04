"""
Backend App Logic
@Author: Umaiza Azmat
@Version: 1.0
@Since: 10/03/2025
Usage:
Embed and secure spotify data
Change Log:
Version 1.0 (10/03/2025):
Created backend code to embed spotify data
"""
# spotify_client.py - minimal wrapper + token refresh stub
import requests
import os
from typing import Optional

SPOTIFY_API = "https://api.spotify.com/v1"
SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"
CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID", "")
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET", "")

def spotify_get(path: str, access_token: str, params: dict = None):
    url = f"{SPOTIFY_API}{path}"
    headers = {"Authorization": f"Bearer {access_token}"}
    r = requests.get(url, headers=headers, params=params, timeout=10)
    if r.status_code == 200:
        return r.json()
    else:
        # return None in skeleton; handle errors in callers
        return {"error": r.status_code, "text": r.text}

def refresh_spotify_token(refresh_token: str) -> Optional[dict]:
    # Stub: implement PKCE / refresh flow for production.
    payload = {"grant_type": "refresh_token", "refresh_token": refresh_token, "client_id": CLIENT_ID}
    r = requests.post(SPOTIFY_TOKEN_URL, data=payload, auth=(CLIENT_ID, CLIENT_SECRET))
    if r.status_code == 200:
        return r.json()
    else:
        return None

