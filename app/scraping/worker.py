from app.scraping import initializer
from app.utils.dados_jogos import championships
from app.scheduler.scheduler import start_scheduler

from concurrent.futures import ThreadPoolExecutor, as_completed
from tenacity import retry, stop_after_attempt, wait_exponential
from func_timeout import func_timeout, FunctionTimedOut
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
    file_path = f"app/data/{championships}.json"
    if not os.path.exists(file_path):
        return True
    try:
        return (time.time() - os.path.getmtime(file_path)) > 3600  # 1 hora
    except:
        return True
    
        

def start_scraping():
    os.makedirs("app/data", exist_ok=True)
    
    pending_championships = [c for c in championships if should_scrape(c)]
    
    if not pending_championships:
        start_scheduler()
        return

    print(f"🚀 Iniciando scraping para {len(pending_championships)} campeonatos...")
    
    with ThreadPoolExecutor(max_workers=2) as executor:
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