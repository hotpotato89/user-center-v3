from fastapi import APIRouter, HTTPException, Depends, Query
from typing import Annotated
from asyncpg import Pool

from app.services.users_services import get_users_service

from app.api.deps import get_pool

router = APIRouter()

@router.get('/users')
async def get_users(pool: Annotated[Pool, Depends(get_pool)],
                    limit: int = Query(..., ge=1, description='Лимит записей в одной странице'),
                    page: int = Query(..., ge=1, description='Какая страница будет просмотрена')):
    limit = min(limit, 50)
    skip = (page-1)*limit

    result = await get_users_service(pool=pool, limit=limit, skip=skip)
    if not result.success:
        if result.error_code == 'empty':
            raise HTTPException(status_code=404, detail=result.message)
        raise HTTPException(status_code=500, detail=result.message)
    return result