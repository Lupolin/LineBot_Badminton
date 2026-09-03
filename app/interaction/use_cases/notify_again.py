from dataclasses import dataclass
from logging import Logger

from domain.gateway import (
    DateTimeCalendarService,
    MessageService,
)
from domain.repository import MemberProfileRepository
from domain.service import MessageGenerator
from infrastructure.opentelemetry import trace_method

from ..dispatcher import UseCaseCommand


@dataclass
class NotifyAgainUseCase:
    member_profile_repo: MemberProfileRepository
    message_service: MessageService
    message_generator: MessageGenerator
    calendar: DateTimeCalendarService
    logger: Logger

    @trace_method("UseCase: NotifyAgainUseCase")
    async def execute(self, cmd: UseCaseCommand) -> str:
        try:
            self.logger.info(f"Executing NotifyAgainUseCase | User: {cmd.user_id} | Intent: {cmd.intent}")

            played_date = self.calendar.get_played_date()
            today_name = self.calendar.get_today_name()
            pending_members = await self.member_profile_repo.get_pending_members()

            reminder_message = self.message_generator.get_reminder_message(
                played_date=played_date,
                today_name=today_name,
            )

            assert cmd.member is not None
            await self.member_profile_repo.save(member=cmd.member)

            for m in pending_members:
                await self.message_service.push_message(
                    user_id=m.user_id,
                    message=reminder_message,
                )

            self.logger.info(f"Notify Again process finished for user: {cmd.user_id}")
            return "Handle notify process successful"

        except Exception as e:
            self.logger.error(
                f"UseCase Error [{type(e).__name__}]: Failed to send notify message for {cmd.user_id} - {str(e)}",
                exc_info=True,
            )
            return "Failed to send notify message to user"
