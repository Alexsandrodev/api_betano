from fastapi import APIRouter
from fastapi.responses import FileResponse
from app.db.operations import load_results
from app.scheduler.first_scheduler import first_scheduler

router = APIRouter()

@router.get("/scrape/{id}")
async def scrape_website(id: str):
    dados = load_results(id)

    return dados

first_scheduler.start()