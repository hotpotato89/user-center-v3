from fastapi import FastAPI
import uvicorn

from app.core.config import settings

app = FastAPI(title='User Center V3')

if __name__ == '__main__':
    uvicorn.run(
        'run:app',
        host='0.0.0.0',
        port=8000,
        reload=settings.debug #type: ignore
    )