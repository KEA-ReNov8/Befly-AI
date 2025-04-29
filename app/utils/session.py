import uuid
from app.core.exceptions import CustomException
from app.repository.chat_repository import ChatRepository


class SessionManager:
    @staticmethod
    def generate_session_id(user_id: str) -> str:
        return f"{user_id}-{uuid.uuid4().hex}"

    @staticmethod
    async def validate_session(session_id: str, user_id: str):
        info = await ChatRepository.find_session_info(session_id)
        if not info:
            raise CustomException(403, "INVALID_SESSION", "세션이 없습니다.")
        if not session_id.startswith(user_id):
            raise CustomException(403, "INVALID_SESSION", "세션이 유효하지 않습니다.")