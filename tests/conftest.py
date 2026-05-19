import pytest
from fastapi.testclient import TestClient
from faker import Faker
from random import randint
import asyncpg

from run import app
from app.core.config import settings
from app.core.database import init_db, DSN

fake = Faker()

@pytest.fixture(scope='session')
async def pool_create():
    pool = await asyncpg.create_pool(DSN, min_size=1, max_size=2)

    async with pool.acquire() as conn:
        await init_db(pool)
    
    yield pool

    async with pool.acquire() as conn:
        await conn.execute('truncate users restart identity')
    await pool.close()

@pytest.fixture
def client(pool_create):
    app.state.pool = pool_create

    with TestClient(app) as client:
        yield client
    
    app.state.pool = None

@pytest.fixture
def password():
    return settings.admin_password

@pytest.fixture
def fake_user():
    data = {
        'name': fake.first_name(),
        'age': randint(1, 120),
        'email': fake.email()
    }
    return data