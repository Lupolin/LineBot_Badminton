from dataclasses import dataclass
from logging import Logger

from domain.repository import MemberProfileRepository
from infrastructure.opentelemetry import trace_method

from ..dispatcher import UseCaseCommand


@dataclass
class HandleAttendanceUseCase:
    member_profile_repo: MemberProfileRepository
    logger: Logger

    @trace_method("UseCase: HandleAttendanceUseCase")  #
    async def execute(self, cmd: UseCaseCommand) -> str:
        try:
            self.logger.info(f"Executing HandleAttendanceUseCase | User: {cmd.user_id} | Intent: {cmd.intent}")

            assert cmd.member is not None

            cmd.member.update_attendance(
                intent=cmd.intent,
                user_content=cmd.user_content,
            )
            await self.member_profile_repo.save(cmd.member)

            self.logger.info(f"Attendance update process finished for user: {cmd.user_id}")
            return "Handle attendance process successful"

        except Exception as e:
            self.logger.error(
                f"UseCase Error [{type(e).__name__}]: Failed to handle attendance for {cmd.user_id} - {str(e)}",
                exc_info=True,
            )
            return "Failed to handle attendance"
