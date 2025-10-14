# routers/compare.py - community comparisons
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..db import get_db
from .. import models, crud
from typing import List

router = APIRouter()

@router.post("/with/{user_id}")
def compare_with(user_id: str, friend_ids: List[str], db: Session = Depends(get_db)):
    """
    Compare user's artist distribution with friends
    """
    # privacy checks omitted for brevity
    def get_artist_set(uid):
        tracks = db.query(models.Track).join(models.Playlist).filter(models.Playlist.user_id == uid).all()
        s = set()
        for t in tracks:
            for a in (t.artist_ids or []):
                s.add(a)
        return s

    base = get_artist_set(user_id)
    results = {"user_count": len(base), "comparisons": {}}
    for fid in friend_ids:
        fset = get_artist_set(fid)
        overlap = base.intersection(fset)
        unique_to_user = base - fset
        unique_to_friend = fset - base
        results["comparisons"][fid] = {"overlap_count": len(overlap), "unique_to_user": len(unique_to_user), "unique_to_friend": len(unique_to_friend)}
    comp = models.Comparison(user_id=user_id, friend_ids=friend_ids, results=results)
    db.add(comp)
    db.commit()
    db.refresh(comp)
    return comp
