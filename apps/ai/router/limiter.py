from .client import RedisClientWrapper

class RateLimiter:
    def __init__(self):
        self.redis = RedisClientWrapper().get_connection()
    
    def is_allowed(self, user_id: str) -> bool:
        key = f"nestbot_cache:limit:{user_id}"
        try:
            # Atomic increment
            count = self.redis.incr(key)
            if count == 1:
                self.redis.expire(key, 60) # Reset every minute
            
            return count <= 20
        except Exception:
            return True # Fail-Open: Allow traffic if Redis is down