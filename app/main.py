from fastapi import FastAPI, Depends
from fastapi.security import APIKeyCookie

from app.api.routes.chat import router as chat_router
from app.core.config import settings
from app.Exception.handlers import setup_exception_handlers


cookie_scheme = APIKeyCookie(name="accessToken", auto_error=False, description="액세스 토큰 (쿠키)")
app = FastAPI(
    title=settings.APP_NAME,
    dependencies=[
        Depends(cookie_scheme)
    ]
)

app.include_router(chat_router)
setup_exception_handlers(app)