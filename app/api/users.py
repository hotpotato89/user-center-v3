from fastapi import APIRouter, HTTPException, Depends
from typing import Annotated
from asyncpg import Pool

from app.services.users_services import get_users_service

from app.api.deps import get_pool

router = APIRouter()

@router.get('/users')
async def get_users(pool: Annotated[Pool, Depends(get_pool)]):
    result = await get_users_service(pool)
    if not result.success:
        if result.error_code == 'empty':
            raise HTTPException(status_code=404, detail=result.message)
        raise HTTPException(status_code=500, detail='Внутрення ошибка сервера')
    return result