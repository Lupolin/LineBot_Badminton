from dataclasses import dataclass
from logging import Logger

from domain.entity import (
    MemberInfo,
    UserIntent,
)
from domain.gateway import (
    MessageService,
)
from domain.repository import (
    AttendanceRecordRepository,
    MemberProfileRepository,
)
from domain.service import MessageGenerator
from infrastructure.opentelemetry import trace_method


@dataclass
class SendTopAbsenteeUseCase:
    member_profile_repo: MemberProfileRepository
    absentee_repo: AttendanceRecordRepository
    message_service: MessageService
    message_generator: MessageGenerator
    logger: Logger

    @trace_method("UseCase: SendTopAbsenteeUseCase")
    async def execute(
        self,
        user_id: str,
        user_content: str,
        reply_token: str,
        intent: UserIntent,
        member: MemberInfo,
    ) -> str:
        try:
            self.logger.info(f"Executing SendTopAbsenteeUseCase | User: {user_id} | Intent: {intent.name}")

            member.update_info(
                intent=intent,
                user_content=user_content,
            )

            raw_list = await self.absentee_repo.find_top_absentees()
            top_absentee_list = raw_list if raw_list is not None else []

            self.logger.info(f"Retrieved {len(top_absentee_list)} absentees from repository")

            message = self.message_generator.get_attendance_result_message(top_absentee_list)

            await self.member_profile_repo.save(member)

            if reply_token:
                await self.message_service.reply_message(
                    reply_token=reply_token,
                    message=message,
                )

            self.logger.info("Send top absentee process finished")
            return message

        except Exception as e:
            self.logger.error(
                f"UseCase Error [{type(e).__name__}]: Failed to send top absentee message to {user_id} - {str(e)}",
                f"Failed to send top absentee message to user: {e}",
                exc_info=True,
            )
            return f"Failed to send top absentee message to user | UserId = {user_id}"
