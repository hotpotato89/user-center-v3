from fastapi import APIRouter, Request, HTTPException
from redis.asyncio import Redis

from app.utils.cache import invalidate_cache

ALLOWED_HOSTS = ['127.0.0.1', '::1', 'localhost', '172.17.0.1', '172.18.0.1']

router = APIRouter(tags=['Test'])

@router.get('/__flush__', description='Нужен для очистки кэша, доступен только локально')
async def flush_redis(request: Request):
    if request.client.host not in ALLOWED_HOSTS: #type: ignore
        raise HTTPException(status_code=403, detail='Доступ закрыт')
    await invalidate_cache(request.app.state.redis)
    return {'status': 'Cleaned'}