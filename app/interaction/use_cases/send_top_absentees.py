from dataclasses import dataclass
from logging import Logger

from domain.gateway import (
    MessagingApiClient,
)
from domain.repository import (
    AttendanceRecordRepository,
    MemberProfileRepository,
)
from domain.service import MessageGenerator
from infrastructure.opentelemetry import trace_method

from ..dispatcher import UseCaseCommand


@dataclass
class SendTopAbsenteeUseCase:
    member_profile_repo: MemberProfileRepository
    attendance_record_repo: AttendanceRecordRepository
    message_service: MessagingApiClient
    message_generator: MessageGenerator
    logger: Logger

    @trace_method("UseCase: SendTopAbsenteeUseCase")
    async def execute(self, cmd: UseCaseCommand) -> str:
        try:
            self.logger.info(f"Executing SendTopAbsenteeUseCase | User: {cmd.user_id} | Intent: {cmd.intent}")

            raw_list = await self.attendance_record_repo.find_top_absentees()
            top_absentee_list = raw_list if raw_list is not None else []

            self.logger.info(f"Retrieved {len(top_absentee_list)} absentees from repository")

            message = self.message_generator.get_attendance_result_message(absentee=top_absentee_list)

            assert cmd.member is not None
            await self.member_profile_repo.save(member=cmd.member)

            if cmd.reply_token:
                await self.message_service.reply_message(
                    reply_token=cmd.reply_token,
                    message=message,
                )

            self.logger.info("Send top absentee process finished")
            return message

        except Exception as e:
            self.logger.error(
                f"UseCase Error [{type(e).__name__}]: Failed to send top absentee message to {cmd.user_id} - {str(e)}",
                f"Failed to send top absentee message to user: {e}",
                exc_info=True,
            )
            return f"Failed to send top absentee message to user | UserId = {cmd.user_id}"
