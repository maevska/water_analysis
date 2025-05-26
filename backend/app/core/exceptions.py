from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError

class WaterQualityException(Exception):
    def __init__(self, status_code: int, detail: str):
        self.status_code = status_code
        self.detail = detail

def setup_exception_handlers(app: FastAPI):
    @app.exception_handler(WaterQualityException)
    async def water_quality_exception_handler(request: Request, exc: WaterQualityException):
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail}
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        return JSONResponse(
            status_code=422,
            content={"detail": str(exc)}
        )

    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception):
        return JSONResponse(
            status_code=500,
            content={"detail": str(exc)}
        ) 