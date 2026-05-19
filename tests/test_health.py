import pytest

@pytest.mark.asyncio
async def test_health(session, url):
    async with session.get(f'{url}/health') as resp:
        assert resp.status == 200
        assert await resp.json() == {'status': 'Healthy'}