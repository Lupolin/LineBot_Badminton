from logging import Logger

from linebot.v3.messaging import ApiClient, Configuration, MessagingApi
from linebot.v3.messaging.models import PushMessageRequest, TextMessage

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
