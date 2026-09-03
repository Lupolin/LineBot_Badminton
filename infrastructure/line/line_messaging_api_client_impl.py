from dataclasses import (
    dataclass,
    field,
)
from logging import Logger

from linebot.v3.messaging import (
    AsyncApiClient,
    AsyncMessagingApi,
    Configuration,
)
from linebot.v3.messaging.models import (
    PushMessageRequest,
    ReplyMessageRequest,
    TextMessage,
)

from domain.gateway import MessagingApiClient
from infrastructure.opentelemetry import trace_method


@dataclass
class LineMessagingApiClientImpl(MessagingApiClient):
    message_api: AsyncMessagingApi = field(init=False)
    access_token: str
    logger: Logger

    def __post_init__(self):
        configuration = Configuration(access_token=self.access_token)
        api_client = AsyncApiClient(configuration=configuration)
        self.message_api = AsyncMessagingApi(api_client)

    @trace_method("Infra: LineMessagingApiClientImpl.push_message")
    async def push_message(
        self,
        user_id: str,
        message: str,
    ):
        try:
            await self.message_api.push_message(
                PushMessageRequest(
                    to=user_id,
                    messages=[TextMessage(text=message)],
                )
            )

            self.logger.info(f"Successfully pushed message to user {user_id}")

        except Exception:
            self.logger.error(f"Failed to push message to {user_id}", exc_info=True)

    @trace_method("Infra: LineMessagingApiClientImpl.reply_message")
    async def reply_message(
        self,
        reply_token: str,
        message: str,
    ):
        """
        使用 reply_token 進行免費回覆
        """
        try:
            await self.message_api.reply_message(
                ReplyMessageRequest(
                    replyToken=reply_token,
                    messages=[TextMessage(text=message)],
                )
            )

            self.logger.info("Successfully replied message")

        except Exception:
            self.logger.error("Failed to reply message", exc_info=True)

    async def close(self):
        try:
            await self.message_api.api_client.close()
            self.logger.info("LINE AsyncApiClient has been closed safely.")
        except Exception as e:
            self.logger.error(f"Error while closing LINE AsyncApiClient: {e}")
