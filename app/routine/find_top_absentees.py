from dataclasses import dataclass
from logging import Logger

from domain.repository import AttendanceRecordRepository
from infrastructure.opentelemetry import trace_method


@dataclass
class FindTopAbsenteesUseCase:
    attendance_record_repo: AttendanceRecordRepository
    logger: Logger

    @trace_method("UseCase: FindTopAbsenteesUseCase")
    async def execute(self):
        self.logger.info("Starting find top absentees process.")

        try:
            result = await self.attendance_record_repo.find_top_absentees()

            self.logger.info("Find top absentees process finished.")
            return result

        except Exception as e:
            self.logger.error(
                f"UseCase Error [{type(e).__name__}]: Failed to find top absentees",
                exc_info=True,
            )
            raise RuntimeError("Failed to find top absentees") from e
