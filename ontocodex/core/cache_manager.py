
import os, json, hashlib, time
from typing import Optional, Any

class OCXCacheManager:
    def __init__(self, base_dir: Optional[str] = None):
        self.base_dir = base_dir or os.path.expanduser("~/.ontocodex/cache")
        os.makedirs(self.base_dir, exist_ok=True)

    def _key(self, term: str, source: str) -> str:
        h = hashlib.sha256(f"{term}::{source}".encode("utf-8")).hexdigest()
        return h[:24]

    def _folder(self, source: str) -> str:
        p = os.path.join(self.base_dir, source.lower())
        os.makedirs(p, exist_ok=True)
        return p

    def path_for(self, term: str, source: str) -> str:
        return os.path.join(self._folder(source), f"{self._key(term, source)}.json")

    def load(self, term: str, source: str, max_age_days: int = 30):
        p = self.path_for(term, source)
        if not os.path.exists(p):
            return None
        age_days = (time.time() - os.path.getmtime(p)) / 86400.0
        if age_days > max_age_days:
            return None
        try:
            with open(p, "r", encoding="utf-8") as f:
                data = json.load(f)
                data["_cache_meta"] = {"path": p, "age_days": age_days}
                return data
        except Exception:
            return None

    def save(self, term: str, source: str, data):
        p = self.path_for(term, source)
        with open(p, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return p
