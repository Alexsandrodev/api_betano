from app.scraping import initializer
from app.utils.game_data import championships_names
from app.scheduler.scheduler import start_scheduler
from app.db.operations import save_data, load_results

from concurrent.futures import ThreadPoolExecutor, as_completed
from tenacity import retry, stop_after_attempt, wait_exponential
from func_timeout import func_timeout, FunctionTimedOut
from datetime import datetime
import time
import os


@retry(stop=stop_after_attempt(3),
       wait=wait_exponential(multiplier=1, min=4, max=10))
def scrape_with_timeout(championships, timeout=300):
    start_time = time.time()
    try:
        result = func_timeout(timeout, initializer.scrape_data, args=(championships,))
        duration = time.time() - start_time
        print(f"[SUCESSO] {championships} completado em {duration:.1f}s")
        return result
    except FunctionTimedOut:
        print(f"[TIMEOUT] {championships} após {timeout}s")
        raise
    except Exception as e:
        print(f"[ERRO] {championships} em {time.time()-start_time:.1f}s: {str(e)}")
        raise

def should_scrape(championships):
    existing_data = load_results(championships)
    if not existing_data:
        return True
    try:
        ultima_atualizacao_ts = datetime.strptime(
                existing_data.get('ultimaAtualizacao', '01/01/1970 00:00:00'),
                '%d/%m/%Y %H:%M:%S'
            ).timestamp()

        return (time.time() - ultima_atualizacao_ts) > 3600
    except:
        return True
    

def start_scraping():
    pending_championships = [c for c in championships_names if should_scrape(c)]
    
    if not pending_championships:
        start_scheduler()
        return

    print(f"🚀 Iniciando scraping para {len(pending_championships)} campeonatos...")
    
    with ThreadPoolExecutor(max_workers=1) as executor:
        futures = {
            executor.submit(scrape_with_timeout, championships): championships
            for championships in pending_championships
        }
        
        for future in as_completed(futures):
            championships = futures[future]
            try:
                future.result()
                print(f"✅ {championships} concluído com sucesso")
            except Exception as e:
                print(f"❌ Falha crítica em {championships}: {str(e)}")
                # Opcional: enviar notificação ou logar erro em banco de dados
    
    start_scheduler()