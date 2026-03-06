import datetime
from logging import Logger

from infrastructure.common import DateTimeCalendarService
from infrastructure.opentelemetry import trace_method


class DateTimeCalendarServiceImpl(DateTimeCalendarService):
    def __init__(
        self,
        logger: Logger,
    ):
        self.logger = logger

    @trace_method("Infra: DateTimeCalendarServiceImpl.played_date")
    def get_played_date(
        self,
        reference_date: datetime.date | None = None,
    ) -> str:
        today = reference_date or datetime.date.today()

        days_until_friday = (4 - today.weekday()) % 7
        played_date = today + datetime.timedelta(days=days_until_friday)

        result = played_date.strftime("%m/%d")

        self.logger.info(f"Calculated played date: {result} (Reference: {today})")

        return result

    @trace_method("Infra: DateTimeCalendarServiceImpl.get_today_name")
    def get_today_name(self, reference_date: datetime.date | None = None) -> str:
        today = reference_date or datetime.date.today()
        result = today.strftime("%A").lower()

        self.logger.info(f"Determined today name: {result}")

        return result
