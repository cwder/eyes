from apscheduler.schedulers.background import BackgroundScheduler

from config.config import EyesConfig
from spider.final_spider import EyesShare
from spider.old_shares_spider import OldShare


def job():
    EyesConfig.initLog()
    info = OldShare()
    info.work()


scheduler = BackgroundScheduler()
scheduler.add_job(job, 'cron', hour=10, minute=0)
