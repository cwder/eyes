from fastapi import FastAPI

import uvicorn

from schedule.daycheduler import scheduler

app = FastAPI()


@app.get("/")
def health():
    return {"love you": "my love eyes"}


scheduler.start()
uvicorn.run(app, host="0.0.0.0", port=9999)
