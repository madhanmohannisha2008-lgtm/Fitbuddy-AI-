import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.routes import router

app = FastAPI(
    title="FitBuddy – AI Fitness Plan Generator",
    description="Personalized 7-day workout plans and nutrition tips powered by Google Gemini",
    version="1.0.0"
)

# Ensure static directory exists so FastAPI doesn't error if empty
os.makedirs("static/images", exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(router)