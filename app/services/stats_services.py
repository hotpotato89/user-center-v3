import asyncpg

from app.schemas.common import ReturnForm

async def get_stats_service(pool):
    async with pool.acquire() as session:
        total_users = await session.fetchval('select count(*) from users')
        if total_users == 0:
            return ReturnForm(success=False, message='База данных пуста', error_code='empty')
        
        oldest_user = await session.fetchrow('select * from users order by age desc limit 1')
        youngest_user = await session.fetchrow('select * from users order by age asc limit 1')
        mean_age = await session.fetchval('select avg(age) from users')
        
        stats = {
            'oldest_user': dict(oldest_user) if oldest_user else None,
            'youngest_user': dict(youngest_user) if youngest_user else None,
            'mean_age': round(mean_age, 2) if mean_age else 0,
            'total_users': total_users
        }
        return ReturnForm(success=True, message='Данные успешно получены', data=stats)