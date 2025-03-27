from apscheduler.schedulers.background import BackgroundScheduler 
from app.scraping.worker import start_scraping
from datetime import datetime, timedelta

first_scheduler = BackgroundScheduler(job_defaults={'misfire_grace_time': 60})
first_scheduler.add_job(
    start_scraping,
    max_instances=1
)