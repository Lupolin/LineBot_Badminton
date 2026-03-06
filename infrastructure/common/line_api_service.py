from abc import ABC, abstractmethod


class LineApiService(ABC):
    @abstractmethod
    def get_user_name(self, user_id: str) -> str:
        pass

    @abstractmethod
    def reply_message(self, reply_token: str, messages: list[dict]) -> None:
        pass
