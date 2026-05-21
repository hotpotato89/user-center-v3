import pytest
import aiohttp
from faker import Faker
from random import randint

from app.core.config import settings

fake = Faker()

@pytest.fixture()
async def session():
    async with aiohttp.ClientSession() as session:
        yield session

@pytest.fixture()
def url():
    return 'http://localhost:8000'

@pytest.fixture()
def password():
    return {
        'password': settings.admin_password
    }

@pytest.fixture()
def fake_user():
    return {
        'name': fake.first_name(),
        'age': randint(1, 120),
        'email': fake.email(),
    }

@pytest.fixture(autouse=True)
async def flush_redis(session, url):
    """Специальная авто-фикстура для очистки кэша"""
    async with session.get(f'{url}/__flush__') as resp:
        assert resp.status == 200
    yield
    async with session.get(f'{url}/__flush__') as resp:
        assert resp.status == 200