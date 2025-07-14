from app.services.news import fetch_newsapi
print("Imported fetch_newsapi successfully")

from fastapi import FastAPI
from app.api.routes import router
from app.db.sqlite import init_db

app = FastAPI(title="Kura-Kani Backend")
app.include_router(router)

@app.on_event("startup")
async def startup() -> None:
    init_db()

@app.get("/")
async def root():
    return {"message": "Kura-Kani Backend is running!"}

