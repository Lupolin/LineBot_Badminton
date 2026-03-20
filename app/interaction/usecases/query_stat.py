from logging import Logger

from domain.interaction.entities import (
    MemberInfo,
    UserIntent,
)
from domain.interaction.repository import UpdateMemberInfoRepository
from domain.routine import (
    GetMemberInfoRepository,
    MessageService,
)
from infrastructure.common import (
    DateTimeCalendarService,
    LineMessageService,
)
from infrastructure.opentelemetry import trace_method


class QueryStatUseCase:
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

    @trace_method("UseCase: QueryStatUseCase")
    def execute(
        self,
        user_id: str,
        user_content: str,
        reply_token: str,
        intent: UserIntent,
        member: MemberInfo,
    ) -> None:
        try:
            self.logger.info(f"QueryStatUseCase: user_id={user_id}, intent={intent}")

            member.update_info(
                intent=intent,
                user_content=user_content,
            )

            played_date = self.calendar.get_played_date()
            attending_members = self.message_repo.get_attending_members()
            not_attending_members = self.message_repo.get_not_attending_members()
            pending_members = self.message_repo.get_pending_members()

            summary_message = self.provider.get_summary_message(
                played_date=played_date,
                attending_members=attending_members,
                not_attending_members=not_attending_members,
                pending_members=pending_members,
            )

            self.member_repo.save(member)

            if reply_token:
                self.messenger.reply_message(
                    reply_token=reply_token,
                    message=summary_message,
                )
            else:
                self.messenger.push_message(
                    user_id=user_id,
                    message=summary_message,
                )

            self.logger.info("Query Stat process finished.")
            return

        except Exception as e:
            raise RuntimeError(f"Error querying stats for user {user_id}") from e
