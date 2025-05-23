from fastapi import FastAPI, Depends
from fastapi.security import APIKeyHeader

from app.api.routes.chat import router as chat_router
from app.core.config import settings
from app.Exception.handlers import setup_exception_handlers


bearer_header = APIKeyHeader(name="Authorization", auto_error=False, description="액세스 토큰 (Bearer 형식)")
app = FastAPI(
    title=settings.APP_NAME,
    dependencies=[
        Depends(bearer_header)
    ]
)

app.include_router(chat_router)
setup_exception_handlers(app)