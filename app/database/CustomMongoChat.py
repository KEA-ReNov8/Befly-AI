from typing import Optional, List
import json
from datetime import datetime
from langchain_core.messages import BaseMessage, message_to_dict, messages_from_dict
from langchain_mongodb import MongoDBChatMessageHistory

from app.core.exceptions import CustomException


class CustomMongoDBChatMessageHistory(MongoDBChatMessageHistory):
    def __init__(
            self,
            session_id: str,
            connection_string: str,
            database_name: str,
            collection_name: str,
            category: Optional[str] = None,
            chat_title: Optional[str] = None,
            after_keyword: Optional[List[str]] = None,
            report: Optional[dict] = None,
            user_id: str = None,
            worry_state: bool = True
    ):
        super().__init__(
            session_id=session_id,
            connection_string=connection_string,
            database_name=database_name,
            collection_name=collection_name,
            session_id_key="session_id",
            history_key="history"
        )
        self.category = category
        self.chat_title = chat_title
        self.after_keyword = after_keyword or []
        self.report = report or {}
        self.user_id = user_id
        self.worry_state = worry_state

    def _session_exists(self) -> bool:
        """세션 존재 여부 확인"""
        return self.collection.find_one({"session_id": self.session_id}) is not None

    def create_session(self) -> None:
        """세션 Document 생성"""
        if self._session_exists():
            # 세션이 이미 있으면 만들지 않음
            return

        session_info = {
            "session_id": self.session_id,
            "user_id": self.user_id,
            "category": self.category,
            "chat_title": self.chat_title,
            "after_keyword": self.after_keyword,
            "report": self.report,
            "created_at": datetime.now(),
            "history": "[]",
            "worry_state": self.worry_state,
        }
        self.collection.insert_one(session_info)

    def add_message(self, message: BaseMessage) -> None:
        """메시지 추가"""
        if not self._session_exists():
            raise CustomException(403,"INVALID_SESSION", "존재하지 않는 세션입니다.")

        # 현재 저장된 메시지 가져오기
        doc = self.collection.find_one({"session_id": self.session_id})
        current_messages = json.loads(doc["history"]) if doc.get("history") else []

        # 새 메시지를 딕셔너리로 변환하여 추가
        message_dict = message_to_dict(message)
        current_messages.append(message_dict)

        # 업데이트
        self.collection.update_one(
            {"session_id": self.session_id},
            {"$set": {"history": json.dumps(current_messages)}}
        )

    @property
    def messages(self) -> List[BaseMessage]:
        """메시지 목록 조회"""
        doc = self.collection.find_one({"session_id": self.session_id})
        if doc is None or not doc.get("history"):
            return []

        try:
            messages_data = json.loads(doc["history"])
            if not isinstance(messages_data, list):
                return []
            return messages_from_dict(messages_data)
        except (json.JSONDecodeError, TypeError):
            return []
