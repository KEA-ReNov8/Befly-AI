from app.database.MongoDB import get_db
from app.core.config import settings

class ChatRepository:
    @staticmethod
    async def find_sessions_by_user(user_id: str):
        db = get_db()
        return await db[settings.MONGODB_COLLECTION].distinct("SessionId", {"user_id": user_id})

    @staticmethod
    async def find_session_info(session_id: str):
        db = get_db()
        return await db[settings.MONGODB_COLLECTION].find_one(
            {"SessionId": session_id},
            sort=[("created_at", -1)]
        )
''