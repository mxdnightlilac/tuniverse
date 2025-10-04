# utils.py - small helpers for enrichment and geocoding (stubs)
import time
from typing import Optional, Dict

def musicbrainz_lookup_artist(name: str) -> Optional[Dict]:
    """
    Stub: replace with real MusicBrainz calls.
    Return a dict like {"country": "GB", "region": "England", "lat": 51.5, "lon": -0.1}
    """
    # naive hack for demo:
    if "beatles" in name.lower():
        return {"country": "GB", "region": "England", "lat": 53.4, "lon": -2.97}
    return None

def geocode_country(country_name: str) -> Optional[Dict]:
    # stub: convert country to approximate lat/lon
    mapping = {"United States": {"lat": 39.8, "lon": -98.6}, "GB": {"lat": 54.0, "lon": -2.0}}
    return mapping.get(country_name) or mapping.get(country_name[:2]) or None

def now_iso():
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
