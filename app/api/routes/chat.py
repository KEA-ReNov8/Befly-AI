from typing import Annotated

from fastapi import APIRouter, Body, Path, Request

from app.models.RequestEntity import ChatMessage, ChatStart
from app.models.ResponseModel import ResponseModel
from app.service.chat_service import ChatService

router = APIRouter(prefix="/consult/chat", tags=["Chat"])


@router.post("/", response_model=ResponseModel)
async def chat(
        request: Request,
        message: Annotated[ChatMessage, Body()]):

    headers = request.headers
    model = await ChatService.process_chat(
        message_content=message.content,
        session_id=message.session_id,
        user_id=headers.get("X-USER-ID")
    )
    return ResponseModel(
        code = "COMMON200",
        message = "채팅 보내기에 성공했습니다.",
        result = model)


@router.post("/new", response_model=ResponseModel)
async def new_chat(request: Request, start: Annotated[ChatStart, Body()]):
    headers = request.headers

    data = await ChatService.create_new_chat(
        user_id=headers.get("X-USER-ID"),
        chat_title=start.chat_title,
        category=start.worry_category
    )
    return ResponseModel(
        code = "Common200",
        message= "새로운 채팅이 생성되었습니다.",
        result = data
    )


@router.get("/history/{session_id}", response_model=ResponseModel)
async def chat_history(
        request: Request,
        session_id: Annotated[str, Path()]
):
    headers = request.headers
    user_id = headers.get("X-USER-ID")
    model = await ChatService.get_chat_history(session_id, user_id)
    return ResponseModel(
        code = "common200",
        message=" 채팅 기록 반환에 성공했습니다.",
        result = model
    )


@router.get("/list/{status_field}", response_model=ResponseModel)
async def chat_list(
        request: Request,
        status_field: Annotated[bool, Path()]
):
    user_id = request.headers.get("X-USER-ID")
    model= await ChatService.get_chat_list(user_id, status_field)
    return ResponseModel(
        code="COMMON200",
        message="채팅 기록 반환에 성공했습니다.",
        result = model
    )


@router.get("/evaluate/{session_id}", response_model=ResponseModel)
async def evaluate_user(
    session_id: Annotated[str, Path()],
    request: Request
):
    user_id = request.headers.get("X-USER-ID")
    model = await ChatService.evaluate_user(session_id, user_id)
    return ResponseModel(
        code="COMMON200",
        message="평가가 완료되었습니다.",
        result = model
    )
@router.delete("/{status_field}/{session_id}/", response_model=ResponseModel)
async def delete_session(
    session_id: Annotated[str, Path()],
    status_field: Annotated[bool, Path()],
    request: Request
):
    user_id = request.headers.get("X-USER-ID")
    if(await ChatService.delete_chat(session_id, user_id, status_field)):
        return ResponseModel(
            code="COMMON200",
            message="채팅이 삭제되었습니다."
        )