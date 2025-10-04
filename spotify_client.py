import requests
import os

SPOTIFY_BASE_URL = "https://api.spotify.com/v1"

def spotify_api_get(endpoint: str, token: str, params=None):
    url = f"{SPOTIFY_BASE_URL}{endpoint}"
    headers = {"Authorization": f"Bearer {token}"}
    r = requests.get(url, headers=headers, params=params)
    if r.status_code == 200:
        return r.json()
    else:
        raise Exception(f"Spotify API error: {r.status_code} {r.text}")
