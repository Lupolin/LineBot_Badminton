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


class SendSummaryUseCase:
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

    @trace_method("UseCase: SendSummaryUseCase")
    def execute(self):
        played_date = self.calendar.get_played_date()
        self.logger.info(f"Starting summary process for game ({played_date}).")

        admin_members = self.repo.get_admin_members()
        attending_members = self.repo.get_attending_members()
        not_attending_members = self.repo.get_not_attending_members()
        pending_members = self.repo.get_pending_members()

        summary_message = self.provider.get_summary_message(
            played_date=played_date,
            attending_members=attending_members,
            not_attending_members=not_attending_members,
            pending_members=pending_members,
        )

        for member in admin_members:
            try:
                self.messenger.push_message(
                    member.user_id,
                    summary_message,
                )
            except Exception:
                self.logger.error(f"Failed to send summary to user {member.user_id}")

        self.logger.info("Summary process finished.")
