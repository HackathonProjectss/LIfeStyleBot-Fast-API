from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseSettings
from typing import List, Dict
from pydantic import AnyHttpUrl
from core.logger import logger
from models.user_model import User
from decouple import config


class Settings(BaseSettings):
    API_V1_STR: str = "/api"
    AUTH0_AUDIENCE: str = config('AUTH0_AUDIENCE', cast=str)
    AUTH0_DOMAIN: str = config('AUTH0_DOMAIN', cast=str)
    AUTH0_ALGORITHMS: str = config('AUTH0_ALGORITHMS', cast=str)
    AUTH0_ISSUER: str = f"https://{AUTH0_DOMAIN}/"
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []
    PROJECT_NAME: str = "LifeStyle"
    MONGODB_CONNECTION_STRING: str = config('MONGODB_CONNECTION_STRING', cast=str)
    BASE_URL: str = config('BASE_URL', cast=str)
    GEMINI_API_KEY: str = config('GEMINI_API_KEY', cast=str)

    class Config:
        case_sensitive = True


settings = Settings()


async def init_db():
    # Initiate connection to MongoDB
    logger.info("Connecting to MongoDB")
    db_client = AsyncIOMotorClient(settings.MONGODB_CONNECTION_STRING).scraper
    # Assuming init_beanie is a function that needs to be called at app startup
    await init_beanie(
        database=db_client,
        document_models=[
            User,  # Ensure User is imported
        ],
    )
    logger.info("Connected to MongoDB")
