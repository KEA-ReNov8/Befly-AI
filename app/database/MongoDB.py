from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings

client = AsyncIOMotorClient(settings.MONGODB_URL)

def get_db():
    return client[settings.MONGODB_DB_NAME]

