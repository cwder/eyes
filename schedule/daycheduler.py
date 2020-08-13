from apscheduler.schedulers.background import BackgroundScheduler

from config.config import EyesConfig
from spider.final_spider import EyesShare
from spider.final_spider2 import EyesShare2
from spider.old_shares_spider import OldShare
from spider.old_shares_spider2 import OldShare2


def job():
    EyesConfig.initLog()
    info = EyesShare2()
    info.run()


scheduler = BackgroundScheduler()
scheduler.add_job(job, 'cron', hour=12, minute=45)
