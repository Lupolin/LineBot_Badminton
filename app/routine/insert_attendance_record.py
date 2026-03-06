from logging import Logger

from domain.routine.repository import AttendanceRecordRepository
from infrastructure.opentelemetry import trace_method


class InsertAttendanceRecordUseCase:
    def __init__(
        self,
        repo: AttendanceRecordRepository,
        logger: Logger,
    ):
        self.repo = repo
        self.logger = logger

    @trace_method("UseCase: InsertAttendanceRecordUseCase")
    def execute(self):
        self.logger.info("Starting insert record to AttendanceRecord")

        try:
            records = self.repo.get_all_data()
            self.repo.save_all(records=records)

            self.logger.info("Insert process finished.")

        except Exception as e:
            raise ValueError("Failed to insert record AttendanceRecord") from e
