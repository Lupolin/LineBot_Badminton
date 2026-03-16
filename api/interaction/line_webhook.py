from fastapi import (
    APIRouter,
    BackgroundTasks,
    Header,
    Request,
)

from app.registry import registry

router = APIRouter()


@router.post(
    "/webhook",
    summary="LINE Webhook 監聽入口",
)
def line_webhook(
    request: Request,
    background_tasks: BackgroundTasks,
    x_line_signature: str = Header(None),
):
    body_dict = request.json()
    events = registry.line_message_handler.parse_webhook_body(body_dict)

    for event in events:
        background_tasks.add_task(
            registry.dispatcher.execute,
            user_id=event.user_id,
            user_content=event.user_content,
            reply_token=event.reply_token,
        )

    return "OK"
