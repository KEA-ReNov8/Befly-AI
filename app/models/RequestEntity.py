from pydantic import BaseModel, Field

class ChatMessage(BaseModel):
    content: str = Field(
        example="안녕, 오늘 날씨 어때?", # <-- 여기에 example 추가!
        description="사용자가 전송하는 채팅 메시지 내용"
    )
    session_id: str = Field(
        ...,
        example="user-session-abc-123", # <-- 여기도 example 추가!
        description="채팅 세션을 식별하는 고유 ID"
    )

class ChatStart(BaseModel):
    chat_title: str  = Field(
        ...,
        example="채팅 제목",
        description="응답 메시지 (성공/실패 여부 및 상세 내용)"
    )
    worry_category: str  = Field(
        ...,
        example="스트레스",
        description="응답 메시지 (성공/실패 여부 및 상세 내용)"
    )