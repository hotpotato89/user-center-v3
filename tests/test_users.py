import pytest

@pytest.mark.asyncio
async def test_add_user(session, url, test_user):
    async with session.post(f'{url}/add_user', json=test_user) as resp:
        assert resp.status == 200
        data = await resp.json()
        assert 'success' in data
        assert 'message' in data
        assert 'id' in data