from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated
from asyncpg import Pool

from app.services.stats_services import get_stats_service

from app.api.deps import get_pool

router = APIRouter(tags=['Stats'])

@router.get('/stats')
async def stats_page(pool: Annotated[Pool, Depends(get_pool)]):
    result = await get_stats_service(pool)
    if not result.success:
        if result.error_code == 'empty':
            raise HTTPException(status_code=404, detail=result.message)
    
    return result