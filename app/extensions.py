import os
import redis

# esto conecta la app con Redis, que es donde se guarda todo / this connects the app to Redis, where everything is stored
r = redis.Redis(
    host=os.environ.get("REDIS_HOST", "localhost"),   # lee el host del sistema / reads host from environment
    port=int(os.environ.get("REDIS_PORT", 6379)),     # lee el puerto del sistema / reads port from environment
    decode_responses=True,                             # para que devuelva texto en vez de bytes / so it returns text instead of raw bytes
)
