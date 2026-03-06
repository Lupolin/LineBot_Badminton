from fastapi import APIRouter

from .handle_mamber_reply import router as intent_router
from .line_webhook import router as line_webhook_router

response_group = APIRouter(prefix="/interaction", tags=["Intent"])
response_group.include_router(intent_router)
response_group.include_router(line_webhook_router)
