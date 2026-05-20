from fastapi import FastAPI
import uvicorn
from contextlib import asynccontextmanager
from redis.asyncio import Redis

from app.core.config import settings
from app.core.database import create_connection, init_db
from app.core.redis_client import create_redis

from app.api.health import router as health_router
from app.api.users import router as users_router
from app.api.stats import router as stats_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.pool = await create_connection()
    await init_db(app.state.pool)

    app.state.redis = await create_redis()
    await app.state.redis.ping() #type: ignore

    yield

    await app.state.redis.close()
    await app.state.pool.close()



app = FastAPI(title='User Center V3', lifespan=lifespan)

app.include_router(health_router)
app.include_router(users_router)
app.include_router(stats_router)

if __name__ == '__main__':
    uvicorn.run(
        'run:app',
        host='0.0.0.0',
        port=8000,
        reload=settings.debug #type: ignore
    )