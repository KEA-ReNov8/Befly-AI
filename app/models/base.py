from pydantic import BaseModel

class CommonResponse(BaseModel):
    code: str = "COMMON200"
    message: str
