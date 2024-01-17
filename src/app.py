from fastapi import FastAPI
from a18_async_iter import router

app = FastAPI(title='Async features')
app.include_router(router)
