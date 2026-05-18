import asyncpg

from app.core.config import settings

DSN = f'postgresql://{settings.db_user}:{settings.db_password}@db/{settings.db_name}'

async def create_connection():
    return await asyncpg.create_pool(DSN, min_size=2, max_size=10)

async def init_db(pool: asyncpg.Pool):
    async with pool.acquire() as conn:
        await conn.execute('create table if not exists users (id serial primary key, name varchar(60), age integer, email varchar(45) unique, reg_time timestamp default now())')
        await conn.execute('create index if not exists idx_regtime_desc on users(reg_time desc)')
        await conn.execute('create index if not exists idx_age on users(age)')