from pydantic import BaseModel
import datetime
from typing import Any

class ResponseModel(BaseModel):
    time: datetime.datetime = datetime.datetime.now()
    code: str
    message: str
    result: Any