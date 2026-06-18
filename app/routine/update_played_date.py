from dataclasses import dataclass
from logging import Logger

from domain.routine.repository import GetMemberInfoRepository
from infrastructure.common import DateTimeCalendarService
from infrastructure.opentelemetry import trace_method


@dataclass
class UpdatePlayedDateUseCase:
    repo: GetMemberInfoRepository
    calendar: DateTimeCalendarService
    logger: Logger

    @trace_method("UseCase: UpdatePlayedDateUseCase")
    async def execute(self):
        played_date = self.calendar.get_played_date()

        try:
            self.logger.info(f"Starting update played date process to [{played_date}] for all members.")

            await self.repo.update_played_date(played_date=played_date)

            self.logger.info("Update played date process finished successfully.")

        except Exception as e:
            self.logger.error(
                f"UseCase Error [{type(e).__name__}]: Failed to update played date to {played_date}",
                exc_info=True
            )
            raise RuntimeError("Failed to update played date") from e
