import redis
import os

REDIS_CONFIG = {
    "host": os.environ.get("REDIS_HOST", "localhost"),
    "port": int(os.environ.get("REDIS_PORT", 6379)),
    "username": os.environ.get("REDIS_USERNAME", ""),
    "password": os.environ.get("REDIS_PASSWORD", ""),
    "decode_responses": True,
    "socket_timeout": 0.05,  # 50ms (Strict timeout)
}

class RedisClientWrapper:
    _pool = None

    def __init__(self):
        # Singleton: Reuse connections to save time
        if not RedisClientWrapper._pool:
            RedisClientWrapper._pool = redis.BlockingConnectionPool(
                **REDIS_CONFIG,
                max_connections=10
            )
        self.client = redis.Redis(connection_pool=RedisClientWrapper._pool)

    def get_connection(self):
        return self.client