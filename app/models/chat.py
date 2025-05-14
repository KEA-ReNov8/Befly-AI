from pydantic import BaseModel, Field

class ChatMessage(BaseModel):
    session_id: str
    content: str

class ChatStart(BaseModel):
    chat_title: str
    worry_category: str

class Chat(BaseModel):
    session_id: str
    user_id: str = Field(..., alias="X-USER-ID")

class UserId(BaseModel):
    user_id: str = Field(..., alias="X-USER-ID")