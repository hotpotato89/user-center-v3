from fastapi import APIRouter, HTTPException, Depends, Query, Request
from typing import Annotated
from asyncpg import Pool

from app.services.users_services import get_users_service, add_user_service, clear_all_service, delete_user_service

from app.schemas.users_schemas import UserDataForm, PasswordForm, DeleteUserForm

from app.api.deps import get_pool

router = APIRouter(tags=['Users'])

@router.get('/users')
async def get_users(request: Request,
                    pool: Annotated[Pool, Depends(get_pool)],
                    limit: int = Query(10, ge=1, description='Лимит записей в одной странице'),
                    page: int = Query(1, ge=1, description='Какая страница будет просмотрена')):
    limit = min(limit, 50)
    skip = (page-1)*limit

    result = await get_users_service(pool=pool, limit=limit, skip=skip)
    if not result.success:
        if result.error_code == 'empty':
            raise HTTPException(status_code=404, detail=result.message)
        raise HTTPException(status_code=500, detail=result.message)
    return result

@router.post('/add_user')
async def add_user(request: Request, pool: Annotated[Pool, Depends(get_pool)], user_data: UserDataForm):
    result = await add_user_service(pool, user_data)
    if result.success != True:
        if result.error_code == 'conflict':
            raise HTTPException(status_code=409, detail=result.message)
        raise HTTPException(status_code=500, detail=result.message)
    return result

@router.delete('/clear')
async def clear_all(request: Request, password: PasswordForm, pool = Depends(get_pool)):
    result = await clear_all_service(pool, password)
    if not result.success:
        if result.error_code == 'unauthorized':
            raise HTTPException(status_code=401, detail=result.message)
        raise HTTPException(status_code=500, detail=result.message)
    return result

@router.delete('/delete_user')
async def delete_user(request: Request, pool: Annotated[Pool, Depends(get_pool)], user_data: DeleteUserForm):
    result = await delete_user_service(pool, user_data)
    if not result.success:
        if result.error_code == 'unauthorized':
            raise HTTPException(status_code=401, detail=result.message)
        if result.error_code == 'unknown_user':
            raise HTTPException(status_code=404, detail=result.message)
        raise HTTPException(status_code=500, detail=result.message)
    return result