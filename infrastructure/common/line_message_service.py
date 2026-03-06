from abc import ABC, abstractmethod


class LineMessageService(ABC):
    @abstractmethod
    def push_message(self, user_id: str, message: str):
        pass
