from typing import Optional

from app.database.MongoDB import get_db
from app.core.config import settings

class ChatRepository:
    @staticmethod
    async def find_sessions_by_user(user_id: str, status_field: Optional[bool] = None):
        db = get_db()
        query = {"user_id": user_id}
        if status_field is not None:
            query["worry_state"] = status_field

        return await db[settings.MONGODB_COLLECTION].distinct("session_id", query)

    @staticmethod
    async def find_session_info(session_id: str, status_field: Optional[bool] = None):
        db = get_db()
        query = {"session_id": session_id}
        if status_field is None or status_field == "":
            query["worry_state"] = True
        else:
            query["worry_state"] = status_field

        return await db[settings.MONGODB_COLLECTION].find_one(
            query,
            sort=[("created_at", -1)]
        )