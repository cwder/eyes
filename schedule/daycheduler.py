from apscheduler.schedulers.background import BackgroundScheduler
from spider.shares_spider import Share


def job():
    info = Share()
    info.work()


scheduler = BackgroundScheduler()
scheduler.add_job(job, 'cron', hour=1, minute=5)
