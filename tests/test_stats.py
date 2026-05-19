import pytest

@pytest.mark.asyncio
async def test_get_stats(session, url, fake_user):
    async with session.post(f'{url}/add_user', json=fake_user) as resp:
        assert resp.status == 200
    async with session.get(f'{url}/stats') as resp:
        assert resp.status == 200
        assert 'data' in await resp.json()

@pytest.mark.asyncio
async def test_get_stats_empty(session, url, password):
    async with session.delete(f'{url}/clear', json=password) as resp:
        assert resp.status == 200
    async with session.get(f'{url}/stats') as resp:
        assert resp.status == 404