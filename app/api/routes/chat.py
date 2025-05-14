from typing import Annotated

from fastapi import APIRouter, Body, Header, Path, Request

from app.models.base import CommonResponse
from app.service.chat_service import ChatService
from typing import Dict


router = APIRouter(prefix="/consult/chat", tags=["Chat"])


@router.post("/", response_model=CommonResponse)
async def chat(request: Request):
    headers = request.headers
    body_data: Dict = await request.json()

    response = await ChatService.process_chat(
        message_content=body_data.get("content"),
        session_id=body_data.get("session_id"),
        user_id=headers.get("X-USER-ID")
    )
    return CommonResponse(message=response)

@router.post("/new", response_model=dict)
async def new_chat(request: Request):
    headers = request.headers
    body_data: Dict = await request.json()

    return await ChatService.create_new_chat(
        user_id=headers.get("X-USER-ID"),
        chat_title=body_data.get("chat_title"),
        category=body_data.get("category"),
    )

@router.get("/history/{session_id}", response_model=dict)
async def chat_history(
        request: Request,
        session_id: Annotated[str, Path()]
):
    headers = request.headers
    user_id = headers.get("X-USER-ID")
    return await ChatService.get_chat_history(session_id, user_id)


@router.get("/list", response_model=list)
async def chat_list(
        request: Request
):
    user_id = request.headers.get("X-USER-ID")
    return await ChatService.get_chat_list(user_id)


@router.get("/evaluate/{session_id}")
async def evaluate_user(
    session_id: Annotated[str, Path()],
    request: Request
):
    user_id = request.headers.get("X-USER-ID")
    return await ChatService.evaluate_user(session_id, user_id)

@router.delete("/{session_id}")
async def delete_session(
    session_id: Annotated[str, Path()],
    request: Request
):
    user_id = request.headers.get("X-USER-ID")
    return await ChatService.delete_chat(session_id, user_id)