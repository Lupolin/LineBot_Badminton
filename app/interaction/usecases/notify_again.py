from logging import Logger

from domain.interaction.entities import (
    MemberInfo,
    UserIntent,
)
from domain.interaction.repository import UpdateMemberInfoRepository
from domain.routine import (
    MessageService,
)
from domain.routine.repository import GetMemberInfoRepository
from infrastructure.common import (
    DateTimeCalendarService,
    LineMessageService,
)
from infrastructure.opentelemetry import trace_method


class NotifyAgainUseCase:
    def __init__(
        self,
        member_repo: UpdateMemberInfoRepository,
        message_repo: GetMemberInfoRepository,
        messenger: LineMessageService,
        provider: MessageService,
        calendar: DateTimeCalendarService,
        logger: Logger,
    ):
        self.member_repo = member_repo
        self.message_repo = message_repo
        self.messenger = messenger
        self.provider = provider
        self.calendar = calendar
        self.logger = logger

    @trace_method("UseCase: NotifyAgainUseCase")
    def execute(
        self,
        user_id: str,
        user_content: str,
        reply_token: str,
        intent: UserIntent,
        member: MemberInfo,
    ):
        try:
            self.logger.info(f"NotifyAgainUseCase: user_id={user_id}, intent={intent}")

            member.update_info(
                intent=intent,
                user_content=user_content,
            )
            played_date = self.calendar.get_played_date()
            today_name = self.calendar.get_today_name()
            pending_members = self.message_repo.get_pending_members()

            reminder_message = self.provider.get_reminder_message(
                played_date=played_date,
                today_name=today_name,
            )

            self.member_repo.save(member)

            for m in pending_members:
                self.messenger.push_message(
                    m.user_id,
                    reminder_message,
                )
            self.logger.info("Notify Again process finished.")
            return

        except Exception as e:
            raise RuntimeError("Failed to send notify message to user") from e
