from logging import Logger

from linebot.v3.messaging import (
    ApiClient,
    Configuration,
    MessagingApi,
)
from linebot.v3.messaging.models import (
    PushMessageRequest,
    ReplyMessageRequest,
    TextMessage,
)

from infrastructure.common import LineMessageService
from infrastructure.opentelemetry import trace_method


class LineMessageServiceImpl(LineMessageService):
    def __init__(
        self,
        access_token: str,
        logger: Logger,
    ):
        configuration = Configuration(access_token=access_token)
        api_client = ApiClient(configuration=configuration)
        self.message_api = MessagingApi(api_client)
        self.logger = logger

    @trace_method("Infra: LineMessageServiceImpl.push_message")
    def push_message(
        self,
        user_id: str,
        message: str,
    ):
        try:
            self.message_api.push_message(
                PushMessageRequest(
                    to=user_id,
                    messages=[TextMessage(text=message)],
                )
            )
            self.logger.info(f"Successfully pushed message to user {user_id}")
        except Exception:
            self.logger.error(f"Failed to push message to {user_id}")

    @trace_method("Infra: LineMessageServiceImpl.reply_message")
    def reply_message(self, reply_token: str, message: str):
        """
        使用 reply_token 進行免費回覆
        """
        try:
            self.message_api.reply_message(
                ReplyMessageRequest(
                    replyToken=reply_token,
                    messages=[TextMessage(text=message)],
                )
            )
            self.logger.info("Successfully replied message")
        except Exception:
            self.logger.error("Failed to reply message")
