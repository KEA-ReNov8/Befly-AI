from pydantic import BaseModel

class ChatMessage(BaseModel):
    session_id: str
    content: str
    user_id: str

class ChatStart(BaseModel):
    user_id: str
    chat_title: str
    worry_category: str

class Chat(BaseModel):
    session_id: str
    user_id: str
