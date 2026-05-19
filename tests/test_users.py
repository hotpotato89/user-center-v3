import pytest

@pytest.mark.asyncio
async def test_add_user(session, url, test_user):
    async with session.post(f'{url}/add_user', json=test_user) as resp:
        assert resp.status == 200
        data = await resp.json()
        assert 'success' in data
        assert 'message' in data
        assert 'id' in data

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