from fastapi import FastAPI, HTTPException
from book_api import router

app = FastAPI()
app.include_router(router)
