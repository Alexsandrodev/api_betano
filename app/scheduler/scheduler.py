from apscheduler.schedulers.background import BackgroundScheduler
from app.utils import game_data
from app.scraping import updater

scheduler = BackgroundScheduler({
    'apscheduler.executors.default': {
        'class': 'apscheduler.executors.pool:ThreadPoolExecutor',
        'max_workers': 1
    },
    'apscheduler.job_defaults.coalesce': True,
    'apscheduler.job_defaults.max_instances': 1
})

for i, championships in enumerate(game_data.championships_names):
    minutos_attr = f"minutos{championships.replace(' ', '')}"
    minutos = getattr(game_data, minutos_attr, [])
    if not minutos:
        continue  
    
    scheduler.add_job(
        updater.schedule_update,
        'cron',
        minute=','.join(map(str, minutos)),
        second=40,
        args=[championships, championships],
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