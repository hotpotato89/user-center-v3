from fastapi import APIRouter
from fastapi.responses import FileResponse
from pathlib import Path

router = APIRouter(tags=['UI'])

@router.get('/')
async def ui():
    return FileResponse(Path('app/static/index.html'))