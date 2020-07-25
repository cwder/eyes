from apscheduler.schedulers.background import BackgroundScheduler
from fishbase import logger

from spider.shares_spider import Share


def job():
    logger.info("job start------------")
    info = Share()
    info.work()


scheduler = BackgroundScheduler()
scheduler.add_job(job, 'cron', hour=1, minute=59)
