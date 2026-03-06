from logging import Logger

from domain.routine import (
    GetMemberInfoRepository,
    MessageService,
)
from infrastructure.common import (
    DateTimeCalendarService,
    LineMessageService,
)
from infrastructure.opentelemetry import trace_method


class SendReminderUseCase:
    def __init__(
        self,
        repo: GetMemberInfoRepository,
        messenger: LineMessageService,
        provider: MessageService,
        calendar: DateTimeCalendarService,
        logger: Logger,
    ):
        self.repo = repo
        self.messenger = messenger
        self.provider = provider
        self.calendar = calendar
        self.logger = logger

    @trace_method("UseCase: SendReminderUseCase")
    def execute(self):
        played_date = self.calendar.get_played_date()
        today_name = self.calendar.get_today_name()

        self.logger.info(f"Starting reminder process for game ({played_date}). Today is {today_name}.")

        pending_members = self.repo.get_pending_members()

        reminder_message = self.provider.get_reminder_message(
            played_date=played_date,
            today_name=today_name,
        )

        for member in pending_members:
            try:
                self.messenger.push_message(
                    member.user_id,
                    reminder_message,
                )
                self.logger.info("Reminder process finished.")
                return

            except Exception as e:
                raise RuntimeError(f"Failed to send reminder to user {member.user_id}") from e
