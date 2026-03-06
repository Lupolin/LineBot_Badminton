import datetime
from abc import ABC, abstractmethod


class DateTimeCalendarService(ABC):
    @abstractmethod
    def get_played_date(self, reference_date: datetime.date | None = None) -> str:
        pass

    @abstractmethod
    def get_today_name(self, reference_date: datetime.date | None = None) -> str:
        pass
