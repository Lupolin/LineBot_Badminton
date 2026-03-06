from fastapi import APIRouter

from .routine_jobs import router as send_message_router

routine_group = APIRouter(prefix="/routine", tags=["Routine"])
routine_group.include_router(send_message_router)
