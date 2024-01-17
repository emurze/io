import asyncio
from fastapi import FastAPI
from a18_async_iter import router

app = FastAPI(title='Async features')
# app.include_router(router)

count = 0


@app.get('/hello')
async def hello() -> dict:
    global count
    count += 1
    return {'count': count}


@app.get('/hello_world')
async def hello() -> dict:
    return {'hello_world': "Hello world!"}
