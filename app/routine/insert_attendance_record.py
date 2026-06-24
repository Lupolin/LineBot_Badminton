from dataclasses import dataclass
from logging import Logger

from domain.repository import AttendanceRecordRepository
from infrastructure.opentelemetry import trace_method


@dataclass
class InsertAttendanceRecordUseCase:
    attendance_record_repo: AttendanceRecordRepository
    logger: Logger

    @trace_method("UseCase: InsertAttendanceRecordUseCase")
    async def execute(self):
        self.logger.info("Starting insert process to AttendanceRecord")

        try:
            records = await self.attendance_record_repo.get_all_data()

            if not records:
                self.logger.info("No active members found to archive")
                return

            await self.attendance_record_repo.save_all(records=records)

            self.logger.info("Insert attendance records process finished")

        except Exception as e:
            self.logger.error(
                f"UseCase Error [{type(e).__name__}]: Failed to insert record to AttendanceRecord",
                exc_info=True,
            )
            raise ValueError("Failed to insert record to AttendanceRecord") from e
