# cache.py - very small in-memory cache fallback (use redis in prod)
import time

class SimpleCache:
    def __init__(self):
        self.store = {}
    def get(self, key):
        item = self.store.get(key)
        if not item: return None
        val, expires = item
        if expires and time.time() > expires:
            del self.store[key]
            return None
        return val
    def set(self, key, val, ttl=None):
        expires = time.time() + ttl if ttl else None
        self.store[key] = (val, expires)
    def delete(self, key):
        if key in self.store:
            del self.store[key]

cache = SimpleCache()
