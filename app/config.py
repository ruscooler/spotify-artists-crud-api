import os
from functools import lru_cache

from pydantic import BaseSettings

from app.utils import get_logger

logger = get_logger(__name__)


class Settings(BaseSettings):
    PG_USER: str = os.getenv("DB_USER", "dbuser")
    PG_PASS: str = os.getenv("DB_PASSWORD", "dbpassword")
    PG_HOST: str = os.getenv("DB_HOST", "localhost")
    PG_DATABASE: str = os.getenv("DB_NAME", "spotifylib")

    ASYNCPG_URL: str = (
        f"postgresql+asyncpg://{PG_USER}:{PG_PASS}@{PG_HOST}:5432/{PG_DATABASE}"
    )

    JWT_SECRET_KEY: str = os.getenv("SECRET_KEY", "")
    JWT_ALGORITHM: str = os.getenv("ALGORITHM", "")
    JWT_ACCESS_TOKE_EXPIRE_MINUTES: int = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 1)

    SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID", "")
    SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET", "")

    class Config:
        env_file = ".env"


@lru_cache
def get_settings():
    logger.info("Loading config settings from the environment...")
    return Settings()
