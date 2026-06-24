from pydantic import BaseModel

from app import registry
from infrastructure.response.schemas import ApiResponse


class IntentRequest(BaseModel):
    user_id: str
    user_content: str
    reply_token: str


async def handle_request(request: IntentRequest):
    data = await registry.dispatcher.execute(
        user_id=request.user_id,
        user_content=request.user_content,
        reply_token=request.reply_token,
    )
    return ApiResponse.success_response(data=data)
