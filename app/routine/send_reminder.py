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
class SendReminderUseCase:
    repo: GetMemberInfoRepository
    messenger: LineMessageService
    provider: MessageService
    calendar: DateTimeCalendarService
    logger: Logger

    @trace_method("UseCase: SendReminderUseCase")
    async def execute(self):
        try:
            played_date = self.calendar.get_played_date()
            today_name = self.calendar.get_today_name()

            self.logger.info(f"Starting reminder process for game ({played_date}) | Today is {today_name}.")

            pending_members = await self.repo.get_pending_members()

            reminder_message = self.provider.get_reminder_message(
                played_date=played_date,
                today_name=today_name,
            )

            success_count = 0
            for member in pending_members:
                try:
                    await self.messenger.push_message(
                        member.user_id,
                        reminder_message,
                    )
                    success_count += 1
                except Exception as e:
                    self.logger.error(
                        f"Failed to push message to {member.user_id} | Error: {type(e).__name__}",
                        exc_info=True
                    )

            self.logger.info(f"Reminder process finished. Sent: {success_count}/{len(pending_members)}")

        except Exception as e:
            self.logger.error(
                f"UseCase Error [{type(e).__name__}]: Critical failure in SendReminderUseCase",
                exc_info=True,
            )
            raise RuntimeError("Critical error during reminder process") from e
