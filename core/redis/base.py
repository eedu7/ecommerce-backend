import json
from typing import Any

from redis.asyncio import Redis


class BaseRedisStore:
    """
    Base Class for Redis-Backend stores with prefix management.
    """

    def __init__(self, redis: Redis, prefix: str) -> None:
        self._redis = redis
        self._prefix = prefix

    def _make_key(self, key: str) -> str:
        return f"{self._prefix}:{key}"

    async def get(self, key: str) -> str | None:
        return await self._redis.get(key)

    async def get_json(self, key: str) -> Any | None:
        raw = await self.get(key)
        return json.loads(raw) if raw is not None else None

    async def set(self, *, key: str, value: str, ttl: int | None = None) -> None:
        if ttl:
            await self._redis.setex(name=key, value=value, time=ttl)
        else:
            await self._redis.set(key, value)

    async def set_json(self, *, key: str, value: Any, ttl: int | None = None) -> None:
        await self.set(key=key, value=json.dumps(value, default=str), ttl=ttl)

    async def remove(self, key: str) -> int:
        return await self._redis.delete(key)

    async def remove_many(self, *keys: str) -> int:
        return await self._redis.delete(*keys) if keys else 0

    async def exists(self, key: str) -> bool:
        return await self._redis.exists(key) == 1

    async def expire(self, key: str, ttl: int) -> bool:
        return await self._redis.expire(key, ttl)

    async def ttl(self, key: str) -> int:
        """
        Returns remaining TTL in seconds.
            -1 = no expiry.
            -2 = key missing
        """
        return await self._redis.ttl(key)

    async def ping(self) -> bool:
        try:
            return await self._redis_.ping()  # type: ignore
        except Exception:
            return False
