from redis.asyncio import Redis

from app.core.config import settings

async def create_redis():
    return await Redis.from_url(settings.redis_url, decode_responses=True)