from typing import Optional, List

from langchain_community.chat_message_histories import MongoDBChatMessageHistory

from app.database.CustomMongo import CustomMongoDBChatMessageHistory
from app.repository.chat_repository import ChatRepository
from app.utils.session import SessionManager
from app.core.config import settings
from app.prompt.prompt import chain_with_history


class ChatService:
    @staticmethod
    async def process_chat(message_content: str, session_id: str, user_id: str):
        await SessionManager.validate_session(session_id, user_id)
        config = {"configurable": {"session_id": session_id}}
        response = await chain_with_history.ainvoke(
            {"input": message_content},
            config=config
        )
        return response

    @staticmethod
    async def create_new_chat(
            user_id: str,
            chat_title: str,
            category: str,
            after_keyword: Optional[List[str]] = None,
            before_keyword: Optional[List[str]] = None,
            report: Optional[dict] = None
    ):
        session_id = SessionManager.generate_session_id(user_id)

        chat_history = CustomMongoDBChatMessageHistory(
            session_id=session_id,
            connection_string=settings.MONGODB_URL,
            database_name=settings.MONGODB_DB_NAME,
            collection_name=settings.MONGODB_COLLECTION,
            category=category,
            chat_title=chat_title,
            after_keyword=after_keyword,
            before_keyword=before_keyword,
            report=report,
            user_id=user_id
        )

        chat_history.create_session()

        return {
            "session_id": session_id,
            "message": "새로운 대화가 시작되었습니다.",
            "redirect": f"/chat/history/{session_id}"
        }

    @staticmethod
    async def get_chat_history(session_id: str, user_id: str):
        await SessionManager.validate_session(session_id, user_id)

        history = MongoDBChatMessageHistory(
            session_id=session_id,
            connection_string=settings.MONGODB_URL,
            database_name=settings.MONGODB_DB_NAME,
            collection_name=settings.MONGODB_COLLECTION,
        )

        if not history.messages:
            return {"messages": []}

        formatted_messages = []
        for msg in history.messages:
            content = getattr(msg, 'content', None)
            if not content and hasattr(msg, 'data'):
                content = msg.data.get('content', '')

            formatted_message = {
                "type": getattr(msg, 'type', 'unknown'),
                "content": content
            }
            formatted_messages.append(formatted_message)

        return {"messages": formatted_messages}

    @staticmethod
    async def get_chat_list(user_id: str):
        sessions = await ChatRepository.find_sessions_by_user(user_id)
        chat_list = []

        for session_id in sessions:
            info = await ChatRepository.find_session_info(session_id)
            if info:
                chat_list.append({
                    "session_id": session_id,
                    "chat_title": info.get("chat_title", "Untitled"),
                    "created_at": info.get("created_at"),
                    "last_message": info.get("content", "")
                })

        return chat_list