from redis.asyncio import Redis

from core.config import config
from core.dependencies.redis import RedisDep
from core.redis import BaseRedisStore


class RevokeTokenStore(BaseRedisStore):
    def __init__(self, redis: Redis, prefix: str) -> None:
        super().__init__(redis, prefix)

    async def revoke(self, jti: str, ttl: int) -> None:
        await self.set(key=self._make_key(jti), value="REVOKED", ttl=ttl)

    async def is_revoked(self, jti: str) -> bool:
        return await self.exists(self._make_key(jti))


def get_revoke_token_store(redis: RedisDep) -> RevokeTokenStore:
    return RevokeTokenStore(redis, config.REDIS_TOKEN_REVOKE_PREFIX)
