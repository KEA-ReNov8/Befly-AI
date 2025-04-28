from langchain_community.chat_message_histories import MongoDBChatMessageHistory
from typing import Optional, List
from datetime import datetime


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
        before_keyword: Optional[List[str]] = None,
        report: Optional[dict] = None
    ):
        super().__init__(
            session_id=session_id,
            connection_string=connection_string,
            database_name=database_name,
            collection_name=collection_name
        )
        self.category = category
        self.chat_title = chat_title
        self.after_keyword = after_keyword or []
        self.before_keyword = before_keyword or []
        self.report = report or {}

    def create_session(self) -> None:
        """세션 정보를 MongoDB에 저장합니다."""
        session_info = {
            "session_id": self.session_id,
            "category": self.category,
            "chat_title": self.chat_title,
            "after_keyword": self.after_keyword,
            "before_keyword": self.before_keyword,
            "report": self.report,
            "created_at": datetime.now()
        }
        self.collection.insert_one(session_info)