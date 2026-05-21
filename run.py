from fastapi import FastAPI, Request
import uvicorn
from contextlib import asynccontextmanager
from typing import Callable
from time import perf_counter

"""Для фронта"""
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path

from app.core.config import settings
from app.core.database import create_connection, init_db
from app.core.redis_client import create_redis

from app.utils.logger import get_logger

from app.api.health import router as health_router
from app.api.users import router as users_router
from app.api.stats import router as stats_router
from app.api.ui import router as ui_router

logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.pool = await create_connection()
    await init_db(app.state.pool)
    logger.info('Пул соединений установлен')

    app.state.redis = await create_redis()
    await app.state.redis.ping() #type: ignore
    logger.info('Соединение с Redis установлено')

    yield

    await app.state.redis.close()
    logger.info('Соединение с Redis разорвано')
    await app.state.pool.close()
    logger.info('Пул соединений разорван')



app = FastAPI(title='User Center V3', lifespan=lifespan)
"""Для фронта"""
app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.middleware('http')
async def log_slow_request(request: Request, call_next: Callable):
    start_time = perf_counter()
    result = await call_next(request)
    duration = perf_counter() - start_time
    if duration > 0.7:
        logger.warning(f'Slow request: {duration:0.2f}')
    return result

app.include_router(health_router)
app.include_router(users_router)
app.include_router(stats_router)
app.include_router(ui_router)

if __name__ == '__main__':
    uvicorn.run(
        'run:app',
        host='0.0.0.0',
        port=8000,
        reload=settings.debug #type: ignore
    )