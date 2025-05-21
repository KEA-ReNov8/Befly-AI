import uuid
from typing import Optional

from app.core.exceptions import CustomException
from app.repository.chat_repository import ChatRepository


class SessionManager:
    @staticmethod
    def generate_session_id(user_id: str) -> str:
        return f"{user_id}-{uuid.uuid4().hex}"

    @staticmethod
    async def validate_session(session_id: str, user_id: str, status: Optional[bool] = True):
        info = await ChatRepository.find_session_info(session_id, status)
        if not info:
            raise CustomException(403, "INVALID_SESSION", "세션이 없습니다.")
        if not session_id.startswith(user_id):
            raise CustomException(403, "INVALID_SESSION", "세션이 유효하지 않습니다.")