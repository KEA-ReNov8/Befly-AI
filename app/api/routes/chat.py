from fastapi import APIRouter, Body, Header, Path
from typing import Annotated
from app.models.chat import ChatMessage, ChatStart
from app.models.base import CommonResponse
from app.service.chat_service import ChatService

router = APIRouter(prefix="/chat", tags=["Chat"])

@router.post("/", response_model=CommonResponse)
async def chat(message: Annotated[ChatMessage, Body()]):
    response = await ChatService.process_chat(
        message_content=message.content,
        session_id=message.session_id,
        user_id=message.user_id
    )
    return CommonResponse(message=response)

@router.post("/new", response_model=dict)
async def new_chat(request: Annotated[ChatStart, Body()]):
    return await ChatService.create_new_chat(
        user_id=request.user_id,
        chat_title=request.chat_title,
        category=request.worry_category
    )

@router.get("/history/{session_id}", response_model=dict)
async def chat_history(
    session_id: Annotated[str, Path()],
    user_id: Annotated[str, Header(convert_underscores=False)]
):
    return await ChatService.get_chat_history(session_id, user_id)

@router.get("/list", response_model=list)
async def chat_list(
    user_id: Annotated[str, Header()]
):
    return await ChatService.get_chat_list(user_id)
