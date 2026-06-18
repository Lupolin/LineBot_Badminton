from fastapi import APIRouter

from .interaction import router as interaction_router
from .routine import router as routine_router

api_router = APIRouter()

api_router.include_router(interaction_router)
api_router.include_router(routine_router)
