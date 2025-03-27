import asyncio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.routes import router
from app.db.database import init_db

app = FastAPI(title= "Web Screping Api", version="1.0")

ALLOWED_ORIGINS = ["http://localhost:8000/bet365/horarios/tabela"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

init_db()