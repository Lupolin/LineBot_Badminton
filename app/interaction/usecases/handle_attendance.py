from dataclasses import dataclass
from logging import Logger

from domain.interaction.entities import (
    MemberInfo,
    UserIntent,
)
from domain.interaction.repository import UpdateMemberInfoRepository
from infrastructure.opentelemetry import trace_method


@dataclass
class HandleAttendanceUseCase:
    member_repo: UpdateMemberInfoRepository
    logger: Logger

    @trace_method("UseCase: HandleAttendanceUseCase")  #
    async def execute(
            self,
            user_id: str,
            user_content: str,
            reply_token: str,
            intent: UserIntent,
            member: MemberInfo,
    ) -> str:
        try:
            self.logger.info(f"Executing HandleAttendanceUseCase | User: {user_id} | Intent: {intent.name}")

            member.update_attendance(
                intent=intent,
                user_content=user_content
            )

            await self.member_repo.save(member)

            self.logger.info(f"Attendance update process finished for user: {user_id}")
            return "Handle attendance process successful"

        except Exception as e:
            self.logger.error(
                f"UseCase Error [{type(e).__name__}]: Failed to handle attendance for {user_id} - {str(e)}",
                exc_info=True,
            )
            return "Failed to handle attendance"
