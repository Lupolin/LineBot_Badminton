from abc import ABC, abstractmethod


class LineMessageHandler(ABC):
    @abstractmethod
    def parse_webhook_body(self, user_id: str) -> str:
        pass
