from fastapi import Request
from fastapi.responses import JSONResponse

from .schemas import ApiResponse


def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=400,
        content=ApiResponse.error_response(f"{str(exc)}").model_dump(),
    )
