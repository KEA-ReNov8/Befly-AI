from typing import Optional

from motor.motor_asyncio import AsyncIOMotorCursor

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
    async def find_session_info(session_id: str, status_field):
        db = get_db()
        query = {"session_id": session_id}

        # status_field가 None이 아니고 빈 문자열이 아닐 때만 worry_state 조건을 추가합니다.
        if status_field is not None and status_field != "":
            query["worry_state"] = status_field

        return await db[settings.MONGODB_COLLECTION].find_one(
            query,
            sort=[("created_at", -1)]
        )

    @staticmethod
    async def get_all_chat(user_id: str):
        db = get_db()
        query = {"user_id": user_id}
        cursor: AsyncIOMotorCursor = db[settings.MONGODB_COLLECTION].find(query, sort=[("created_at", -1)])
        chat_docs = await cursor.to_list(length=None)
        print(f"Found {len(chat_docs)} chats for user_id: {user_id}")
        return chat_docs