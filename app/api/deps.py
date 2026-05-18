from fastapi import Request
from asyncpg import Pool

async def get_pool(request: Request) -> Pool:
    return request.app.state.pool