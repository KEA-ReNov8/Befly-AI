import json
from typing import Optional, List

from fastapi import status
from starlette.responses import JSONResponse

from app.core.config import settings
from app.core.exceptions import CustomException
from app.database.CustomMongoChat import CustomMongoDBChatMessageHistory
from app.database.MongoDB import get_db
from app.prompt.counselorAI import chain_with_history
from app.prompt.evaulatorAI import evaluation_with_history
from app.repository.chat_repository import ChatRepository
from app.utils.session import SessionManager


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
            report: Optional[dict] = None
    ):
        session_id = SessionManager.generate_session_id(user_id)

        chat_history = CustomMongoDBChatMessageHistory(
            connection_string=settings.MONGODB_URL,
            database_name=settings.MONGODB_DB_NAME,
            collection_name=settings.MONGODB_COLLECTION,
            category=category,
            session_id=session_id,
            chat_title=chat_title,
            after_keyword=after_keyword,
            report=report,
            user_id=user_id,
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

        history = CustomMongoDBChatMessageHistory(
            session_id=session_id,
            connection_string=settings.MONGODB_URL,
            database_name=settings.MONGODB_DB_NAME,
            collection_name=settings.MONGODB_COLLECTION,
            user_id=user_id
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
    async def get_chat_list(user_id: str, status_field: bool):
        print(f"유저 아이디:{user_id}")
        sessions = await ChatRepository.find_sessions_by_user(user_id, status_field)
        print("세션:")
        print(sessions)
        chat_list = []

        for session_id in sessions:
            info = await ChatRepository.find_session_info(session_id, status_field)
            if info:
                chat_list.append({
                    "session_id": session_id,
                    "chat_title": info.get("chat_title", "Untitled"),
                    "created_at": info.get("created_at"),
                    "last_message": info.get("content", ""),
                    "category": info.get("category", ""),
                    "status": info.get("worry_state")
                })

        return chat_list

    @staticmethod
    async def evaluate_user(session_id: str, user_id: str):
        try:
            await SessionManager.validate_session(session_id, user_id)
            config = {"configurable": {"session_id": session_id}}
            response = await evaluation_with_history.ainvoke(
                {"input": "사용자 평가를 시작합니다."},
                config=config,
            )
            try:
                block = parse_json_block(response)
                result = await update_after_keyword_and_change_status(session_id, block)
                if result == "OK":
                    user_info = await ChatRepository.find_session_info(session_id, False)
                    if user_info:  # userInfo가 None이 아닌 경우에만 접근
                        block["worry_title"] = user_info.get("chat_title")
                        block["worry_category"] = user_info.get("category")
                        block["worry_created_at"] = user_info.get("created_at")
                        return block
                    return None  # userInfo가 None인 경우 명시적으로 None 반환
                return None
            except ValueError as e:
                raise CustomException(400, "CHAT003", f"AI 응답에서 JSON 파싱 오류가 발생했습니다: {e}")
        except CustomException as e:
            raise e

    @staticmethod
    async def delete_chat(session_id: str, user_id: str, status: bool):
        await SessionManager.validate_session(session_id, user_id, status)
        try:
            history = CustomMongoDBChatMessageHistory(
                session_id=session_id,
                connection_string=settings.MONGODB_URL,
                database_name=settings.MONGODB_DB_NAME,
                collection_name=settings.MONGODB_COLLECTION,
            )
            history.clear()
            return True
        except Exception as e:
            raise CustomException(500, "CHAT002", "서버 내부 오류입니다.")








def parse_json_block(response_text: str) -> dict:
    import json
    clean = response_text.replace("```json\n", "").replace("\n```", "")
    if not clean:
        raise ValueError("응답에서 JSON 블록을 찾을 수 없습니다.")

    return json.loads(clean)


async def update_after_keyword_and_change_status(session_id: str, data_dict: dict):
    try:
        analytics_data = data_dict.get('analytics', [])

        keywords_to_add = []
        for item in analytics_data:
            keyword_entry = {
                "emotion": item.get('emotion'),
                "score": item.get('score'),
                "comment": item.get('comment')
            }
            keywords_to_add.append(keyword_entry)

        db = get_db()
        collection = db[settings.MONGODB_COLLECTION]
        query = {"session_id": session_id}
        update = {"$push": {"after_keyword": {"$each": keywords_to_add}}, "$set": {"worry_state": False}}
        result = await collection.update_one(query, update)
        if result.modified_count > 0 or result.upserted_id is not None:
            return "OK"
        return None
    except Exception as e:
        print(e)
        raise CustomException(500, "CHAT002", "채팅 세션 업데이트 중 오류가 발생했습니다.")