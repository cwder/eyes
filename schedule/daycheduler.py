import datetime

from apscheduler.schedulers.background import BackgroundScheduler

from bs.building import Build
from config.config import EyesConfig



def job():
    EyesConfig.initLog()
    c = Build()
    c.run()


scheduler = BackgroundScheduler()
scheduler.add_job(job, 'cron', hour=23, minute=20)
# scheduler.add_job(job, 'cron', hour=18, minute=00)
# scheduler.add_job(job, 'interval', seconds=36000, next_run_time=datetime.datetime.now())
