from fastapi import FastAPI

# from spider.shares_spider import Share
import uvicorn

app = FastAPI()


@app.get("/")
def health():
    return {"love you": "my eyes"}


uvicorn.run(app, host="0.0.0.0", port=9999)
# if __name__ == '__main__':
#     info = Share()
#     info.work()
