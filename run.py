from fastapi import FastAPI
import uvicorn

from app.core.config import settings

from app.api.health import router as health_router

app = FastAPI(title='User Center V3')

app.include_router(health_router)

if __name__ == '__main__':
    uvicorn.run(
        'run:app',
        host='0.0.0.0',
        port=8000,
        reload=settings.debug #type: ignore
    )