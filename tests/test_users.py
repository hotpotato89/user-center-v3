import pytest

from app.schemas.users_schemas import DeleteUserForm

@pytest.mark.asyncio
async def test_add_user(session, url, fake_user):
    async with session.post(f'{url}/add_user', json=fake_user) as resp:
        assert resp.status == 200
        data = await resp.json()
        assert 'success' in data
        assert 'message' in data
        assert 'id' in data

@pytest.mark.asyncio
async def test_add_user_conflict_error(session, url, fake_user):
    user = fake_user

    async with session.post(f'{url}/add_user', json=user) as resp:
        assert resp.status == 200
    async with session.post(f'{url}/add_user', json=user) as resp:
        assert resp.status == 409
        data = await resp.json()
        assert 'уже существует' in data['detail']

@pytest.mark.asyncio
async def test_add_user_validate_error(session, url):
    async with session.post(f'{url}/add_user') as resp:
        assert resp.status == 422

@pytest.mark.asyncio
async def test_get_users(session, url):
    async with session.get(f'{url}/users?limit=1&page=1') as resp:
        assert resp.status == 200
        data = await resp.json()
        assert data['success'] == True
        assert 'data' in data

@pytest.mark.asyncio
async def test_get_users_empty(session, url, password):
    async with session.delete(f'{url}/clear', json=password) as resp:
        assert resp.status == 200
    async with session.get(f'{url}/users?limit=1&page=1') as resp:
        assert resp.status == 404

@pytest.mark.asyncio
async def test_clear_db(session, url, password):
    async with session.delete(f'{url}/clear', json=password) as resp:
        assert resp.status == 200
        data = await resp.json()
        assert 'Удалено' in data['message']

@pytest.mark.asyncio
async def test_clear_db_unauthorized_error(session, url):
    wrong = {
        'password': 'wrong-password'
    }
    async with session.delete(f'{url}/clear', json=wrong) as resp:
        assert resp.status == 401

@pytest.mark.asyncio
async def test_clear_db_validate_error(session, url):
    async with session.delete(f'{url}/clear') as resp:
        assert resp.status == 422

@pytest.mark.asyncio
async def test_delete_user(session, url, password, fake_user):
    async with session.post(f'{url}/add_user', json=fake_user) as resp:
        assert resp.status == 200
        user_data = await resp.json()
        user_id = user_data['id']
    delete_form = {
        'id': user_id,
        'password': password['password']
    }
    async with session.delete(f'{url}/delete_user', json=delete_form) as resp:
        assert resp.status == 200
        data = await resp.json()
        assert 'Удален' in data['message']

@pytest.mark.asyncio
async def test_delete_user_unknown_error(session, url, password):
    delete_form = {
        'id': 2100000000,
        'password': password['password']
    }
    async with session.delete(f'{url}/delete_user', json=delete_form) as resp:
        assert resp.status == 404
        data = await resp.json()
        assert 'Нет' in data['detail']

async def test_delete_user_validation_error(session, url):
    async with session.delete(f'{url}/delete_user') as resp:
        assert resp.status == 422