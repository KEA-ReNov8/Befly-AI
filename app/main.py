from fastapi import FastAPI
from app.api.routes.chat import router as chat_router
from app.core.config import settings
from app.core.handlers import setup_exception_handlers

app = FastAPI(title=settings.APP_NAME)

app.include_router(chat_router)
setup_exception_handlers(app)
