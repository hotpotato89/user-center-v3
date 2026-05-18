import asyncpg

from app.schemas.common import ReturnForm

async def get_users_service(pool: asyncpg.Pool, limit: int, skip: int):
    async with pool.acquire() as conn:
        data = await conn.fetch('select * from users order by reg_time desc offset $1 limit $2', skip, limit)
        total = await conn.fetchval('select count(*) from users')
    current_page = (skip // limit) + 1 if limit>0 else 1
    total_pages = (total + limit - 1) // limit if limit > 0 else 1
    if not data:
        return ReturnForm(success=False, message='База данных пуста', error_code='empty')
    return ReturnForm(success=True, message=f'Найдено {len(data)} пользователей.', data=[dict(row) for row in data], total=total, page=current_page, total_pages=total_pages, limit=limit)