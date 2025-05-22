from pydantic import BaseModel, Field
import datetime
from typing import Any

class ResponseModel(BaseModel):
    # Field(default_factory=...)를 사용하여 인스턴스 생성 시점에 현재 시각이 할당되도록 합니다.
    time: datetime.datetime = Field(
        default_factory=datetime.datetime.now,
        description="응답이 생성된 시각"
    )
    code: str = Field(
        ..., # 필수 필드임을 의미
        description="응답 코드 (예: COMMON200, ERROR400)"
    )
    message: str = Field(
        ...,
        description="응답 메시지 (성공/실패 여부 및 상세 내용)"
    )
    result: Any = Field(
        None, # 기본값은 None, 데이터가 없을 수도 있으므로
        description="API 호출 결과 데이터. 채팅 응답 등이 포함됩니다."
    )