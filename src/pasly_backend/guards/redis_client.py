import os
import redis

REDIS_URL = os.environ.get("PASSLY_REDIS_URL", "redis://localhost:6379")

_client: redis.Redis | None = None


def get_redis() -> redis.Redis:
    global _client
    if _client is None:
        _client = redis.Redis.from_url(REDIS_URL, decode_responses=True)
    return _client


def blacklist_token(token: str, ttl_seconds: int) -> None:
    if ttl_seconds > 0:
        get_redis().setex(f"blacklist:{token}", ttl_seconds, "1")


def is_token_blacklisted(token: str) -> bool:
    return get_redis().exists(f"blacklist:{token}") == 1