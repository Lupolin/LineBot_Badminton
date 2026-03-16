from fastapi import APIRouter, status
from pydantic import BaseModel

from app.registry import registry
from infrastructure.opentelemetry import trace_method
from infrastructure.response.schemas import ApiResponse

router = APIRouter()


class IntentRequest(BaseModel):
    user_id: str
    user_content: str


@router.post(
    "/intent",
    status_code=status.HTTP_200_OK,
    summary="處理使用者傳送訊息",
    description="依據使用者傳送的訊息決定執行哪一個UseCase",
    response_model=ApiResponse[bool],
)
@trace_method("API: HandleMemberReply")
def handle_request(request: IntentRequest):
    registry.dispatcher.execute(
        user_id=request.user_id,
        user_content=request.user_content,
    )
    return ApiResponse.success_response(data=True)
