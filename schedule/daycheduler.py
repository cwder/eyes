from apscheduler.schedulers.background import BackgroundScheduler
from fishbase import logger

from config.config import EyesConfig
from spider.shares_spider import Share


def job():
    EyesConfig.initLog()
    info = Share()
    info.parseAll()
    info.processTable()


scheduler = BackgroundScheduler()
scheduler.add_job(job, 'cron', hour=11, minute=20)
