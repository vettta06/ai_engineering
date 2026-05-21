import logging
import sys
from pathlib import Path

from fastapi import FastAPI

from .dependencies import model_service
from .endpoints import router

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)

app = FastAPI(
    title="Credit Scoring API",
    description="API for credit risk prediction",
    version="1.0.0",
)

app.include_router(router, prefix="/api/v1")

PROJECT_DIR = Path(__file__).resolve().parent.parent.parent


@app.on_event("startup")
async def startup_event():
    """Initialize model service on application startup."""
    model_service.initialize(PROJECT_DIR)


@app.get("/")
async def root():
    """Return API root information."""
    return {"service": "Credit Scoring API", "version": "1.0.0", "docs": "/docs"}
