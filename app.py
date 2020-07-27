import time

from fastapi import FastAPI

import uvicorn
from fishbase import logger

from config.config import EyesConfig
from schedule.daycheduler import scheduler
from spider.shares_spider import Share

app = FastAPI()


@app.get("/")
def health():
    logger.info("health------------")
    try:
        info = Share()
        info.work()
    except Exception as ex:
        logger.info("health--ex---------- " + str(ex))
    a = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    return {"love you": "my and you eyes test " + a}


scheduler.start()
uvicorn.run(app, host="0.0.0.0", port=9999)
