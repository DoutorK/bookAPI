from fastapi import FastAPI, HTTPException
from book_api import router
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI()
app.include_router(router)

Instrumentator().instrument(app).expose(app)