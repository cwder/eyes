from apscheduler.schedulers.background import BackgroundScheduler

from config.config import EyesConfig
from spider.final_spider import EyesShare
from spider.old_shares_spider import OldShare
from spider.old_shares_spider2 import OldShare2


def job():
    EyesConfig.initLog()
    info = EyesShare()
    info.work()


scheduler = BackgroundScheduler()
scheduler.add_job(job, 'cron', hour=23, minute=30)
