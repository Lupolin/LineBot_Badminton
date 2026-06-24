from dataclasses import dataclass
from logging import Logger
from typing import ClassVar

from domain.gateway import ApiService
from infrastructure.http import HttpContext
from infrastructure.opentelemetry import trace_method
from infrastructure.setting import config


@dataclass
class LineApiServiceImpl(ApiService):
    logger: Logger
    http: HttpContext
    _headers: ClassVar[dict[str, str]] = {
        "Authorization": f"Bearer {config.LINE_BOT.CHANNEL_ACCESS_TOKEN}",
        "Content-Type": "application/json",
    }

    @trace_method("Infra: LineApiServiceImpl.get_user_name")
    async def get_user_name(self, user_id: str) -> str:
        url = f"{config.LINE_BOT.PROFILE_ENDPOINT}/{user_id}"

        try:
            session = await self.http.get_session()
            async with session.get(url, headers=self._headers) as response:
                if response.status == 200:
                    data = await response.json()
                    return data.get("displayName", user_id)

                self.logger.warning(f"LINE API 查詢失敗, Status: {response.status}, UserID: {user_id}")
                return user_id

        except Exception as e:
            self.logger.error(f"LINE API 連線異常: {str(e)}", exc_info=True)
            return user_id

    @trace_method("Infra: LineApiServiceImpl.reply_message")
    async def reply_message(self, reply_token: str, reply_content: str) -> None:
        url = config.LINE_BOT.REPLY_ENDPOINT
        payload = {"replyToken": reply_token, "messages": [{"type": "text", "text": reply_content}]}

        try:
            session = await self.http.get_session()
            async with session.post(url, headers=self._headers, json=payload) as response:
                response.raise_for_status()
                self.logger.info("Successfully replied to user via pooled session")

        except Exception as e:
            self.logger.error(f"LINE Reply unexpected error: {str(e)}", exc_info=True)
            raise ConnectionError("LINE Reply 失敗") from e
