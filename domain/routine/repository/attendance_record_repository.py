from abc import ABC, abstractmethod

from domain.routine.entities import Attendance


class AttendanceRecordRepository(ABC):
    @abstractmethod
    def save_all(self, records: list[Attendance]) -> None:
        pass

    @abstractmethod
    def get_all_data(self) -> list[Attendance]:
        pass
