from apscheduler.schedulers.background import BackgroundScheduler

from config.config import EyesConfig
from spider.cwd import Cwd
from spider.final_spider import EyesShare
from spider.final_spider2 import EyesShare2
from spider.old_shares_spider import OldShare
from spider.old_shares_spider2 import OldShare2


def job():
    EyesConfig.initLog()
    c = Cwd()
    c.run()


scheduler = BackgroundScheduler()
scheduler.add_job(job, 'cron', hour=23, minute=40)
