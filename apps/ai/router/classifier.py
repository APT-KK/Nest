import hashlib
from .client import RedisClientWrapper

class IntentRouter:
    def __init__(self):
        self.redis = RedisClientWrapper().get_connection()

    def get_intent(self, query: str) -> str:
        # 1. Hashing for Cache Key
        query_hash = hashlib.sha256(query.lower().strip().encode()).hexdigest()
        cache_key = f"nestbot_cache:intent:{query_hash}"

        # 2. CIRCUIT BREAKER / CACHE CHECK
        try:
            cached_intent = self.redis.get(cache_key)
            if cached_intent:
                return cached_intent
        except Exception:
            pass  # Fail-Open: If Redis dies, just continue.

        # 3. HEURISTICS (The "Rule-Based" Brain)
        static_keywords = ["leader", "maintainer", "version", "cve", "github"]
        intent = "DYNAMIC" # Default
        if any(w in query.lower() for w in static_keywords):
            intent = "STATIC"

        # 4. WRITE BACK TO CACHE
        try:
            self.redis.set(cache_key, intent, ex=3600) # Expire in 1 hour
        except Exception:
            pass

        return intent