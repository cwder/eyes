from apscheduler.schedulers.background import BackgroundScheduler
from fishbase import logger

from config.config import EyesConfig
from spider.old_shares_spider import OldShare
from spider.shares_spider import Share
from spider.t_shares_spider import OldAShare


def job():
    EyesConfig.initLog()
    info = OldAShare()
    info.test()


scheduler = BackgroundScheduler()
scheduler.add_job(job, 'cron', hour=16, minute=00)
