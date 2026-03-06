from fastapi import APIRouter

from .interaction import response_group
from .routine import routine_group

api_router = APIRouter()

# 掛載後，路徑會變成 /api/send/...
api_router.include_router(routine_group)
api_router.include_router(response_group)
