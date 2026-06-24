from abc import ABC, abstractmethod


class MessageService(ABC):
    @abstractmethod
    async def push_message(self, user_id: str, message: str):
        pass

    @abstractmethod
    async def reply_message(self, reply_token: str, message: str):
        pass

    @abstractmethod
    async def close(self):
        pass
