import json
from functools import wraps
from redis.asyncio import Redis
from fastapi import Request
from typing import Callable

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
                return await func(*args, **kwargs)
            
            redis: Redis = request.app.state.redis
            cache_key = f'{func.__name__}:{request.url.path}:{request.query_params}'

            cached = await redis.get(cache_key)
            if cached:
                return json.loads(cached)
            
            result = await func(*args, **kwargs)

            if result:
                data = result.dict() if hasattr(result, 'dict') else result
                await redis.setex(cache_key, ttl, json.dumps(data))
            
            return result
        return inner
    return wrapper