from typing import Annotated

from pydantic import BaseModel, Field

from app import registry
from app.interaction.dispatcher import IntentDispatcherCommand
from infrastructure.response.schemas import ApiResponse


class HandelRequestPayload(BaseModel):
    user_id: Annotated[str, Field(alias="userId")]
    user_content: Annotated[str, Field(alias="userContent")]
    reply_token: Annotated[str, Field(alias="replyToken")]


async def handle_request(payload: HandelRequestPayload):
    data = await registry.dispatcher.execute(
        IntentDispatcherCommand(
            user_id=payload.user_id,
            user_content=payload.user_content,
            reply_token=payload.reply_token,
        )
    )
    return ApiResponse.success_response(data=data)
