from typing import Annotated

from fastapi import APIRouter, Body, Path, Request

from app.models.RequestEntity import ChatMessage, ChatStart
from app.models.ResponseModel import ResponseModel
from app.service.chat_service import ChatService

router = APIRouter(prefix="/consult/chat", tags=["Chat"])


@router.post("/", response_model=ResponseModel,
             summary="메시지 전송",  # Swagger UI에 표시될 짧은 요약
             description="사용자로부터 채팅 메시지를 받아 AI의 응답을 반환합니다. 세션 기반으로 대화를 이어나갈 수 있습니다.",  # 자세한 설명
             )
async def chat(
        request: Request,
        message: Annotated[ChatMessage, Body(
            ...,
            description="요청 객체에 대한 설명입니다."
        )]):

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


@router.post("/new", response_model=ResponseModel,
             summary="채팅 생성",
             description="새로운 채팅방을 생성하는 API"
             )
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


@router.get("/history/{session_id}",
            response_model=ResponseModel,
            summary="채팅 기록 조회",
            description="특정 세션 ID에 해당하는 채팅 기록을 조회합니다.",
)
async def chat_history(
        request: Request,
        session_id: Annotated[str, Path(
            ...,
            description="조회하려는 채팅의 고유 식별자입니다. 1은 user의 번호이고, 뒤는 세션입니다. 모두 입력해야 합니다.",
            example="1-7b5297dd568c41dfba9ca419f6b75690",
        )],
):
    headers = request.headers
    user_id = headers.get("X-USER-ID")
    model = await ChatService.get_chat_history(session_id, user_id)
    return ResponseModel(
        code = "common200",
        message=" 채팅 기록 반환에 성공했습니다.",
        result = model
    )


@router.get("/list/{status_field}",
            response_model=ResponseModel,
            summary="채팅방 목록 조회",
            description="해당 유저의 채팅 목록을 조회합니다.",
            )
async def chat_list(
        request: Request,
        status_field: Annotated[bool, Path(
            description="상담이 종료되었을 경우 false, 상담중인 경우 true입니다",
            example="true or false"
        )]
):
    user_id = request.headers.get("X-USER-ID")
    model= await ChatService.get_chat_list(user_id, status_field)
    return ResponseModel(
        code="COMMON200",
        message="채팅 기록 반환에 성공했습니다.",
        result = model
    )


@router.get("/evaluate/{session_id}",
            response_model=ResponseModel,
            summary="상담 평가",
            description="지금까지의 채팅 내용을 평가합니다."
            )
async def evaluate_user(
    session_id: Annotated[str, Path(
        description="조회하려는 채팅의 고유 식별자입니다. 1은 user의 번호이고, 뒤는 세션입니다. 모두 입력해야 합니다.",
        example="1-7b5297dd568c41dfba9ca419f6b75690",
    )],
    request: Request
):
    user_id = request.headers.get("X-USER-ID")
    model = await ChatService.evaluate_user(session_id, user_id)
    return ResponseModel(
        code="COMMON200",
        message="평가가 완료되었습니다.",
        result = model
    )
@router.delete("/{status_field}/{session_id}/",
               response_model=ResponseModel,
               summary="채팅 삭제",
               description="해당 채팅방을 삭제합니다."
               )
async def delete_session(
    session_id: Annotated[str, Path(
        description="삭제하려는 채팅의 고유 식별자입니다. 1은 user의 번호이고, 뒤는 세션입니다. 모두 입력해야 합니다.",
        example="1-7b5297dd568c41dfba9ca419f6b75690"
    )],
    status_field: Annotated[bool, Path(
        description="삭제하려는 채팅 세션의 활성 여부입니다. 상담중인 경우 true, 상담이 종료되었을 경우 false입니다.",
        example="true or false"
    )],
    request: Request
):
    user_id = request.headers.get("X-USER-ID")
    if await ChatService.delete_chat(session_id, user_id, status_field):
        return ResponseModel(
            code="COMMON200",
            message="채팅이 삭제되었습니다."
        )
    return None