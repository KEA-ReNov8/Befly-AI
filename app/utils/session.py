import uuid
from app.core.exceptions import CustomException

class SessionManager:
    @staticmethod
    def generate_session_id(user_id: str) -> str:
        return f"{user_id}-{uuid.uuid4().hex}"

    @staticmethod
    async def validate_session(session_id: str, user_id: str):
        if not session_id.startswith(user_id):
            raise CustomException(403, "INVALID_SESSION", "세션이 유효하지 않습니다.")
