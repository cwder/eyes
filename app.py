import time

from fastapi import FastAPI

import uvicorn
from fishbase import logger

from config.config import EyesConfig
from schedule.daycheduler import scheduler

app = FastAPI()


@app.get("/")
def health():
    a = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    return {"love you": "my and you eyes test " + a}


scheduler.start()
uvicorn.run(app, host="0.0.0.0", port=9999)
