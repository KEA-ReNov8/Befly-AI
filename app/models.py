from pydantic import BaseModel
from typing import Dict, List, Optional

class ChatMessage(BaseModel):
    content: str

class EvaluationResult(BaseModel):
    keyword: str
    score: float
    details: Dict[str, int]

class ChatResponse(BaseModel):
    message: str
    evaluation: Optional[List[EvaluationResult]] = None