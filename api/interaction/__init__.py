from fastapi import APIRouter

from .handle_request import handle_request
from .line_webhook import line_webhook

router = APIRouter(
    prefix="/interaction",
    tags=["Intent"],
)

router.add_api_route(
    "/HandleRequest",
    handle_request,
    methods=["POST"],
    summary="處理使用者傳送訊息",
)

router.add_api_route(
    "/LineWebhook",
    line_webhook,
    methods=["POST"],
    summary="LINE Webhook 監聽入口",
)
