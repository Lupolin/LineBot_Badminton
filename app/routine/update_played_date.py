from logging import Logger

from domain.routine.repository import GetMemberInfoRepository
from infrastructure.common import DateTimeCalendarService
from infrastructure.opentelemetry import trace_method


class UpdatePlayedDateUseCase:
    def __init__(
        self,
        repo: GetMemberInfoRepository,
        calendar: DateTimeCalendarService,
        logger: Logger,
    ):
        self.repo = repo
        self.calendar = calendar
        self.logger = logger

    @trace_method("UseCase: ResetAttendanceUseCase")
    def execute(self):
        played_date = self.calendar.get_played_date()

        self.logger.info("Starting update played date process for all members.")

        try:
            self.repo.update_played_date(played_date=played_date)

        except Exception as e:
            raise RuntimeError("Failed to update played date") from e
