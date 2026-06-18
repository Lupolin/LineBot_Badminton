from dataclasses import dataclass
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


@dataclass
class QueryStatUseCase:
    member_repo: UpdateMemberInfoRepository
    message_repo: GetMemberInfoRepository
    messenger: LineMessageService
    provider: MessageService
    calendar: DateTimeCalendarService
    logger: Logger

    @trace_method("UseCase: QueryStatUseCase")
    async def execute(
        self,
        user_id: str,
        user_content: str,
        reply_token: str,
        intent: UserIntent,
        member: MemberInfo,
    ) -> str:
        try:
            self.logger.info(f"Executing QueryStatUseCase | User: {user_id} | Intent: {intent.name}")

            member.update_info(
                intent=intent,
                user_content=user_content,
            )

            played_date = self.calendar.get_played_date()
            attending_members = await self.message_repo.get_attending_members()
            not_attending_members = await self.message_repo.get_not_attending_members()
            pending_members = await self.message_repo.get_pending_members()

            message = self.provider.get_summary_message(
                played_date=played_date,
                attending_members=attending_members,
                not_attending_members=not_attending_members,
                pending_members=pending_members,
            )

            await self.member_repo.save(member)

            if reply_token:
                await self.messenger.reply_message(
                    reply_token=reply_token,
                    message=message,
                )

            self.logger.info(f"Query Stat process finished for user: {user_id}")
            return message

        except Exception as e:
            self.logger.error(
                f"UseCase Error [{type(e).__name__}]: Failed to handle querying stats for {user_id} - {str(e)}",
                exc_info=True,
            )
            return "Failed to handle querying stats"
