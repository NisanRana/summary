from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.api.routes import router as news_router
from app.services.auth import router as auth_router
from app.db.sqlite import init_db
from dotenv import load_dotenv
import logging
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handle startup and shutdown events."""
    logger.info("Starting up KuraKani Backend")
    init_db()  # Initialize SQLite database
    yield
    logger.info("Shutting down KuraKani Backend")

# Initialize FastAPI app
app = FastAPI(
    title="KuraKani News Summarizer",
    description="Backend for KuraKani news summarizer web app",
    version="1.0.0",
    lifespan=lifespan
)

# Include routers
app.include_router(news_router)
app.include_router(auth_router)

@app.get("/")
async def root():
    """Root endpoint for KuraKani Backend."""
    return {"message": "KuraKani Backend is running!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8000)))