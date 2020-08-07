from apscheduler.schedulers.background import BackgroundScheduler

from config.config import EyesConfig
from spider.final_spider import EyesShare


def job():
    EyesConfig.initLog()
    info = EyesShare()
    info.run()


scheduler = BackgroundScheduler()
scheduler.add_job(job, 'cron', hour=18, minute=0)
