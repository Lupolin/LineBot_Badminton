from dataclasses import dataclass
from logging import Logger

from domain.routine.repository import GetMemberInfoRepository
from infrastructure.opentelemetry import trace_method


@dataclass
class ResetAttendanceUseCase:
    repo: GetMemberInfoRepository
    logger: Logger

    @trace_method("UseCase: ResetAttendanceUseCase")
    async def execute(self):
        self.logger.info("Starting attendance reset process for all members")

        try:
            await self.repo.reset_all_attendance()

            self.logger.info("Attendance reset process finished")

        except Exception as e:
            self.logger.error(
                f"UseCase Error [{type(e).__name__}]: Failed to reset attendance",
                exc_info=True,
            )
            raise RuntimeError("Failed to reset attendance") from e
