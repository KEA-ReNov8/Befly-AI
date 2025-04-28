from fastapi import Request
from fastapi.responses import JSONResponse
from app.core.exceptions import CustomException, ServerException

def setup_exception_handlers(app):
    @app.exception_handler(CustomException)
    async def custom_exception_handler(request: Request, exc: CustomException):
        return JSONResponse(
            status_code=exc.status_code,
            content={"code": exc.code, "message": exc.message}
        )

    @app.exception_handler(ServerException)
    async def server_exception_handler(request: Request, exc: ServerException):
        return JSONResponse(
            status_code=500,
            content={"code": exc.code, "message": exc.message}
        )
