import asyncio
import multiprocessing
from fastapi import APIRouter, BackgroundTasks
from fastapi.responses import FileResponse

from app.scraping import inicializador
from app.utils.dados_jogos import campeonatos
from app.scheduler.scheduler import scheduler

import os
import time

router = APIRouter()

def scrape_wrapper(campeonato):
    inicializador.scrape_data(campeonato)
    

def run_scrape(campeonato):
    """Função que roda o scrape em um processo separado."""
    scrape_wrapper(campeonato)

def processar_com_semaforo(campeonato, semaforo):
    with semaforo:  # Garante que só dois processos rodarão ao mesmo tempo
        run_scrape(campeonato)

def start_scraping():
    """Inicia processos de scraping para campeonatos pendentes, limitando a 2 processos simultâneos e aguarda sua conclusão."""
    campeonatos_pendentes = [c for c in campeonatos if not os.path.exists(f"{c}.json")]
    
    if campeonatos_pendentes:
        semaforo = multiprocessing.Semaphore(2)  # Limita a no máximo 2 processos simultâneos
        processos = []

        for campeonato in campeonatos_pendentes:
            # Agora passamos a função globalizada e o semáforo como argumentos
            p = multiprocessing.Process(target=processar_com_semaforo, args=(campeonato, semaforo))
            p.start()
            processos.append(p)

        # Aguarda todos os processos terminarem
        for p in processos:
            p.join()



async def wait_for_file(file_path, timeout=60):
    """Espera o arquivo ser criado, com timeout de 60 segundos."""
    for _ in range(timeout):
        if os.path.exists(file_path):
            return True
        await asyncio.sleep(1)
    return False


@router.get("/scrape/{id}")
async def scrape_website(id: str, background_tasks: BackgroundTasks):
    id = f"{id}.json"

    start_scraping()

    # if not scheduler.running:  
    #     print("Iniciando scheduler...")
    #     scheduler.start()

    
    return FileResponse(id, media_type="application/json")

