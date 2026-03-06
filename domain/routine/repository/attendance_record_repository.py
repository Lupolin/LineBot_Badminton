from abc import ABC, abstractmethod

from domain.routine.entities import AttendanceRecord


class AttendanceRecordRepository(ABC):
    @abstractmethod
    def save_all(self, records: list[AttendanceRecord]) -> None:
        pass

    @abstractmethod
    def get_all_data(self) -> list[AttendanceRecord]:
        pass
