import asyncio

from fastapi import FastAPI

from app.api.artist import router as artist_router
from app.background import runner
from app.utils import get_logger

logger = get_logger(__name__)

app = FastAPI(title="Spotify Artists CRUD API", version="0.11")
app.include_router(artist_router)


@app.on_event("startup")
async def startup_event():
    logger.info("Starting up...")
    asyncio.create_task(runner.run_background())
    logger.info("Starting up...")


@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Shutting down...")
