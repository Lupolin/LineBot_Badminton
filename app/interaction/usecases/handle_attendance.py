from logging import Logger

from domain.interaction.entities import (
    MemberInfo,
    UserIntent,
)
from domain.interaction.repository import UpdateMemberInfoRepository
from infrastructure.opentelemetry import trace_method


class HandleAttendanceUseCase:
    def __init__(
        self,
        member_repo: UpdateMemberInfoRepository,
        logger: Logger,
    ):
        self.member_repo = member_repo
        self.logger = logger

    @trace_method("UseCase: HandleAttendanceUseCase")  #
    def execute(
        self,
        user_id: str,
        user_content: str,
        reply_token: str,
        intent: UserIntent,
        member: MemberInfo,
    ) -> None:
        self.logger.info(f"HandleAttendanceUseCase: user_id={user_id}, intent={intent}")

        try:
            member.update_attendance(intent, user_content)
            self.member_repo.save(member)
            self.logger.info("Reminder process finished.")
            return

        except Exception as e:
            raise RuntimeError(f"Error handling attendance for user {user_id}") from e
