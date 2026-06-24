from abc import ABC, abstractmethod


class MessageHandler(ABC):
    @abstractmethod
    async def parse_webhook_body(self, user_id: str) -> str:
        pass
