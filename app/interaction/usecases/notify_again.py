from dataclasses import dataclass
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


@dataclass
class NotifyAgainUseCase:
    member_repo: UpdateMemberInfoRepository
    message_repo: GetMemberInfoRepository
    messenger: LineMessageService
    provider: MessageService
    calendar: DateTimeCalendarService
    logger: Logger

    @trace_method("UseCase: NotifyAgainUseCase")
    async def execute(
        self,
        user_id: str,
        user_content: str,
        reply_token: str,
        intent: UserIntent,
        member: MemberInfo,
    ) -> str:
        try:
            self.logger.info(f"Executing NotifyAgainUseCase | User: {user_id} | Intent: {intent.name}")

            member.update_info(
                intent=intent,
                user_content=user_content,
            )

            played_date = self.calendar.get_played_date()
            today_name = self.calendar.get_today_name()
            pending_members = await self.message_repo.get_pending_members()

            reminder_message = self.provider.get_reminder_message(
                played_date=played_date,
                today_name=today_name,
            )

            await self.member_repo.save(member)

            for m in pending_members:
                await self.messenger.push_message(
                    m.user_id,
                    reminder_message,
                )

            self.logger.info(f"Notify Again process finished for user: {user_id}")
            return "Handle notify process successful"

        except Exception as e:
            self.logger.error(
                f"UseCase Error [{type(e).__name__}]: Failed to send notify message for {user_id} - {str(e)}",
                exc_info=True,
            )
            return "Failed to send notify message to user"
