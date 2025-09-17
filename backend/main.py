"""
MyOwnGuru - Main application entry point
"""
# Reload trigger: updated at runtime to pick up new .env
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.core.config import settings
from app.api.api_v1.api import api_router
from app.core.database import engine
from app.models import Base
from pathlib import Path
import logging

# Ensure important directories exist
Path("static").mkdir(exist_ok=True)
Path("uploads").mkdir(exist_ok=True)

# Create database tables (non-fatal if DB is unavailable)
try:
    Base.metadata.create_all(bind=engine)
except Exception as e:
    logging.warning(f"Database unavailable during startup: {e}. API will still start; health and non-DB endpoints will function.")

app = FastAPI(
    title="MyOwnGuru API",
    description="Agentic AI platform for personalized professional development",
    version="1.0.0",
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Set up CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API router
app.include_router(api_router, prefix=settings.API_V1_STR)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def root():
    return {
        "message": "Welcome to MyOwnGuru API",
        "version": "1.0.0",
        "docs": "/docs",
        "status": "active"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "MyOwnGuru API"}

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level="info"
    )
