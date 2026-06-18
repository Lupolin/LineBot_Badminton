from dataclasses import dataclass
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


@dataclass
class SendSummaryUseCase:
    repo: GetMemberInfoRepository
    messenger: LineMessageService
    provider: MessageService
    calendar: DateTimeCalendarService
    logger: Logger

    @trace_method("UseCase: SendSummaryUseCase")
    async def execute(self) -> None:
        try:
            played_date = self.calendar.get_played_date()

            self.logger.info(f"Starting summary process for game ({played_date}).")

            admin_members = await self.repo.get_admin_members()
            attending_members = await self.repo.get_attending_members()
            not_attending_members = await self.repo.get_not_attending_members()
            pending_members = await self.repo.get_pending_members()

            summary_message = self.provider.get_summary_message(
                played_date=played_date,
                attending_members=attending_members,
                not_attending_members=not_attending_members,
                pending_members=pending_members,
            )

            success_count = 0
            for member in admin_members:
                try:
                    await self.messenger.push_message(
                        member.user_id,
                        summary_message,
                    )
                    success_count += 1
                except Exception as e:
                    self.logger.error(
                        f"Failed to send summary to admin {member.user_id} | Error: {type(e).__name__}",
                        exc_info=True,
                    )

            self.logger.info(f"Summary process finished. Sent: {success_count}/{len(admin_members)}")

        except Exception as e:
            self.logger.error(
                f"UseCase Error [{type(e).__name__}]: Critical failure in SendSummaryUseCase",
                exc_info=True,
            )
            raise RuntimeError("Critical error during summary sending process") from e
