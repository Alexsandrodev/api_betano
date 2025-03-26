from fastapi import APIRouter
from fastapi.responses import FileResponse

from app.scheduler.first_scheduler import first_scheduler

router = APIRouter()

@router.get("/scrape/{id}")
async def scrape_website(id: str):
    id = f"{id}.json"

    return FileResponse(id, media_type="application/json")

first_scheduler.start()

