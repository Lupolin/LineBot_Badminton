from abc import ABC, abstractmethod


class ApiService(ABC):
    @abstractmethod
    async def get_user_name(self, user_id: str) -> str:
        pass

    @abstractmethod
    async def reply_message(self, reply_token: str, messages: list[dict]) -> None:
        pass
