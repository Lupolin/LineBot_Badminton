from dataclasses import dataclass
from logging import Logger

from domain.repository import AttendanceRecordRepository
from infrastructure.opentelemetry import trace_method


@dataclass
class FindAttendanceRecordUseCase:
    attendance_record_repo: AttendanceRecordRepository
    logger: Logger

    @trace_method("UseCase: FindAttendanceRecordUseCase")
    async def execute(self):
        self.logger.info("Starting find attendance record process")

        try:
            result = await self.attendance_record_repo.find_all_data()

            self.logger.info("Find find attendance record finished")
            return result

        except Exception as e:
            self.logger.error(
                f"UseCase Error [{type(e).__name__}]: Failed to find attendance records",
                exc_info=True,
            )
            raise RuntimeError("Failed to find top absentees") from e
