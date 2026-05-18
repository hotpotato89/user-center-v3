import asyncpg

from app.schemas.common import ReturnForm

async def get_users_service(pool: asyncpg.Pool) -> ReturnForm:
    async with pool.acquire() as conn:
        data = await conn.fetch('select * from users')
    
    if not data:
        return ReturnForm(
            success=False,
            message='База данных пуста',
            error_code='empty',
        )

    return ReturnForm(
        success=True,
        message='Данные получены успешно!',
        data=[dict(row) for row in data],
    )