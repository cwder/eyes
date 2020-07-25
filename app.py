from fastapi import FastAPI

import uvicorn
from fishbase import logger

from schedule.daycheduler import scheduler

app = FastAPI()


@app.get("/")
def health():
    logger.info("health------------")
    return {"love you": "my and you eyes"}


scheduler.start()
uvicorn.run(app, host="0.0.0.0", port=9999)
