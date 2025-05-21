from pydantic import BaseModel


class ChatMessage(BaseModel):
    session_id: str
    content: str

class ChatStart(BaseModel):
    chat_title: str
    worry_category: str