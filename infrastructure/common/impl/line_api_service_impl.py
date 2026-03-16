from logging import Logger

import requests

from infrastructure.common import LineApiService
from infrastructure.opentelemetry import trace_method
from infrastructure.setting.config import config


class LineApiServiceImpl(LineApiService):
    def __init__(
        self,
        logger: Logger,
    ):
        self._headers = {
            "Authorization": f"Bearer {config.LINE_BOT.CHANNEL_ACCESS_TOKEN}",
            "Content-Type": "application/json",
        }
        self.logger = logger

    @trace_method("Infra: LineApiServiceImpl.get_user_name")
    def get_user_name(self, user_id: str) -> str:
        url = f"{config.LINE_BOT.PROFILE_ENDPOINT}/{user_id}"

        try:
            response = requests.get(url, headers=self._headers, timeout=5)
            if response.status_code == 200:
                data = response.json()
                return data.get("displayName", user_id)

            self.logger.warning(f"LINE API 查詢失敗, Status: {response.status_code}, UserID: {user_id}")
            return user_id
        except Exception as e:
            self.logger.error(f"LINE API 連線異常: {e}")
            return user_id

    @trace_method("Infra: LineApiServiceImpl.reply_message")
    def reply_message(self, reply_token: str, reply_content: str) -> None:
        url = config.LINE_BOT.REPLY_ENDPOINT
        payload = {"replyToken": reply_token, "messages": [{"type": "text", "text": reply_content}]}
        try:
            response = requests.post(
                url,
                headers=self._headers,
                json=payload,
                timeout=5,
            )
            response.raise_for_status()
            self.logger.info(f"Successfully replied with token: {reply_token}")
        except Exception as e:
            raise ConnectionError(f"LINE Reply 失敗: {str(e)}") from e
