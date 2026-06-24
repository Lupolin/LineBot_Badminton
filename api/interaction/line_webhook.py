from fastapi import (
    BackgroundTasks,
    Header,
    Request,
)

from app import registry as app_regsitry
from infrastructure import registry as infra_regsitry


async def line_webhook(
    request: Request,
    background_tasks: BackgroundTasks,
    x_line_signature: str = Header(None),
):
    body_dict = await request.json()
    events = await infra_regsitry.line_message_handler.parse_webhook_body(body_dict)

    for event in events:
        background_tasks.add_task(
            app_regsitry.dispatcher.execute,
            user_id=event.user_id,
            user_content=event.user_content,
            reply_token=event.reply_token,
        )

    return "OK"
