from dataclasses import dataclass
from logging import Logger

from domain.entity import MessageEvent
from domain.gateway import WebhookEventParser
from infrastructure.opentelemetry import trace_method


@dataclass
class LineWebhookEventParserImpl(WebhookEventParser):
    logger: Logger

    @trace_method("Infra: LineAdapterImpl.parse_webhook_body")
    async def parse_webhook_body(self, body: dict) -> list[MessageEvent]:
        events = body.get("events", [])
        parsed_events = []

        for event in events:
            if event.get("type") == "message" and event.get("message", {}).get("type") == "text":
                try:
                    user_id = event["source"]["userId"]
                    content = event["message"]["text"]
                    token = event["replyToken"]

                    parsed_events.append(
                        MessageEvent(
                            user_id=str(user_id),
                            user_content=str(content).strip(),
                            reply_token=str(token),
                        )
                    )
                except KeyError as e:
                    self.logger.warning(f"LINE 封包解析失敗，缺少關鍵欄位: {e}")
                    continue

        return parsed_events
