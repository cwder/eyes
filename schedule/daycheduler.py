from apscheduler.schedulers.background import BackgroundScheduler

from config.config import EyesConfig
from spider.final_spider import EyesShare


def job():
    EyesConfig.initLog()
    info = EyesShare()
    info.run()


scheduler = BackgroundScheduler()
scheduler.add_job(job, 'cron', hour=9, minute=35)
scheduler.add_job(job, 'cron', hour=10, minute=35)
