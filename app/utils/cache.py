import json
from functools import wraps
from redis.asyncio import Redis
from fastapi import Request
from typing import Callable

from app.utils.logger import get_logger

logger = get_logger(__name__)

def cache(ttl: int = 60):
    def wrapper(func: Callable):
        @wraps(func)
        async def inner(*args, **kwargs):
            request = None
            for arg in args:
                if isinstance(arg, Request):
                    request = arg
                    break
            
            if not request:
                for value in kwargs.values():
                    if isinstance(value, Request):
                        request = value
                        break
            
            if not request:
                logger.warning('Request не обнаружен')
                return await func(*args, **kwargs)
            
            redis: Redis = request.app.state.redis
            cache_key = f'{func.__name__}:{request.url.path}:{request.query_params}'

            cached = await redis.get(cache_key)
            if cached:
                logger.info(f'Кэш HIT: {cache_key}')
                return json.loads(cached)
            
            result = await func(*args, **kwargs)
            logger.info(f'Кэш  MISS: {cache_key}')

            if result:
                data = result.dict() if hasattr(result, 'dict') else result
                await redis.setex(cache_key, ttl, json.dumps(data, default=str))
                logger.info(f'Кэш сохранен: {cache_key}')
            
            return result
        return inner
    return wrapper

async def invalidate_cache(redis: Redis):
    """Очищение кэша"""
    await redis.flushall()
    logger.info(f'Кэш очищен')