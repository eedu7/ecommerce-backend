from typing import AsyncGenerator

from redis.asyncio import ConnectionPool, Redis
from redis.exceptions import RedisError

from core.config import config
from core.exceptions import InternalServerException

redis_pool: ConnectionPool = ConnectionPool(
    host=config.REDIS_HOST,
    port=config.REDIS_PORT,
    db=config.REDIS_DB,
    password=config.REDIS_PASSWORD,
    max_connections=config.REDIS_MAX_CONNECTIONS,
    socket_timeout=config.REDIS_SOCKET_TIMEOUT,
    socket_connect_timeout=config.REDIS_SOCKET_CONNECT_TIMEOUT,
    decode_responses=config.REDIS_DECODE_RESPONSES,
    health_check_interval=config.REDIS_HEALTH_CHECK_INTERVAL,
)

redis_client: Redis = Redis(connection_pool=redis_pool)


async def get_redis() -> AsyncGenerator[Redis, None]:
    try:
        yield redis_client
    except RedisError as exc:
        raise InternalServerException(details={"reason": str(exc)})
    finally:
        await redis_client.close()
