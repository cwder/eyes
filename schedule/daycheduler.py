from apscheduler.schedulers.background import BackgroundScheduler
from fishbase import logger

from config.config import EyesConfig
from spider.shares_spider import Share


def job():
    EyesConfig.initLog()
    logger.info("job start ============")
    info = Share()
    info.work()


scheduler = BackgroundScheduler()
scheduler.add_job(job, 'cron', hour=21, minute=42)
