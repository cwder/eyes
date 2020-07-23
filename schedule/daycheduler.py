from apscheduler.schedulers.background import BackgroundScheduler
from spider.shares_spider import Share


def job():
    info = Share()
    info.work()


scheduler = BackgroundScheduler()
scheduler.add_job(job, 'cron', hour=16, minute=00)
