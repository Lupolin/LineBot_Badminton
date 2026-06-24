from abc import ABC, abstractmethod

from domain.entity import (
    Absentee,
    Attendance,
)


class AttendanceRecordRepository(ABC):
    @abstractmethod
    async def save_all(self, records: list[Attendance]) -> None:
        pass

    @abstractmethod
    async def get_all_data(self) -> list[Attendance]:
        pass

    @abstractmethod
    async def find_all_data(self) -> list[Attendance] | None:
        pass

    @abstractmethod
    async def find_top_absentees(self) -> list[Absentee] | None:
        pass
