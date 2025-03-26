from apscheduler.schedulers.background import BackgroundScheduler
from app.utils import dados_jogos
from app.scraping import updater

scheduler = BackgroundScheduler({
    'apscheduler.executors.default': {
        'class': 'apscheduler.executors.pool:ThreadPoolExecutor',
        'max_workers': 2
    },
    'apscheduler.job_defaults.coalesce': True,
    'apscheduler.job_defaults.max_instances': 1
})

for i, championships in enumerate(dados_jogos.championships):
    minutos_attr = f"minutos{championships.replace(' ', '')}"
    minutos = getattr(dados_jogos, minutos_attr, [])
    if not minutos:
        continue  
    
    scheduler.add_job(
        updater.agendamento_atualizacao,
        'cron',
        minute=','.join(map(str, minutos)),
        second=40,
        args=[championships, f"{championships.lower().replace(' ', '_')}.json"],
        executor='default',
        misfire_grace_time=120,
        name=f"job_{championships}"
    )


def start_scheduler():
    if not scheduler.running:
        try:
            scheduler.start()
            print("scheduler iniciado")
            return True
        except:
            return False
    return True