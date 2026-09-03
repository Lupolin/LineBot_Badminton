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
class QueryStatUseCase:
    member_profile_repo: MemberProfileRepository
    message_service: MessageService
    message_generator: MessageGenerator
    calendar: DateTimeCalendarService
    logger: Logger

    @trace_method("UseCase: QueryStatUseCase")
    async def execute(self, cmd: UseCaseCommand) -> str:
        try:
            self.logger.info(f"Executing QueryStatUseCase | User: {cmd.user_id} | Intent: {cmd.intent}")

            played_date = self.calendar.get_played_date()
            attending_members = await self.member_profile_repo.get_attending_members()
            not_attending_members = await self.member_profile_repo.get_not_attending_members()
            pending_members = await self.member_profile_repo.get_pending_members()

            message = self.message_generator.get_summary_message(
                played_date=played_date,
                attending_members=attending_members,
                not_attending_members=not_attending_members,
                pending_members=pending_members,
            )

            assert cmd.member is not None
            await self.member_profile_repo.save(member=cmd.member)

            if cmd.reply_token:
                await self.message_service.reply_message(
                    reply_token=cmd.reply_token,
                    message=message,
                )

            self.logger.info(f"Query Stat process finished for user: {cmd.user_id}")
            return message

        except Exception as e:
            self.logger.error(
                f"UseCase Error [{type(e).__name__}]: Failed to handle querying stats for {cmd.user_id} - {str(e)}",
                exc_info=True,
            )
            return "Failed to handle querying stats"
