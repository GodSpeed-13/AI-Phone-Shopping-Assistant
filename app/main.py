from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.api.chat import router as chat_router

app = FastAPI(title="AI Shopping Chat Agent")

app.include_router(chat_router, prefix="/chat")

app.mount("/", StaticFiles(directory="ui", html=True), name="ui")
