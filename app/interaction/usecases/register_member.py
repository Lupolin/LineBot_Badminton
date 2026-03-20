from logging import Logger

from domain.interaction.entities import (
    MemberInfo,
    UserIntent,
)
from domain.interaction.repository import UpdateMemberInfoRepository
from infrastructure.opentelemetry import trace_method


class RegisterMemberUseCase:
    def __init__(
        self,
        member_repo: UpdateMemberInfoRepository,
        line_api_service,
        logger: Logger,
    ):
        self.member_repo = member_repo
        self.line_api_service = line_api_service
        self.logger = logger

    @trace_method("UseCase: RegisterMemberUseCase")
    def execute(
            self, user_id: str,
            user_content: str,
            intent: UserIntent,
            member: MemberInfo,
    ) -> None:
        self.logger.info(f"RegisterMemberUseCase: user_id={user_id}, intent={intent}")

        is_admin_request = user_content == "註冊Admin"
        role = "Admin" if is_admin_request else "Member"

        try:
            user_name = self.line_api_service.get_user_name(user_id)

            member = MemberInfo(
                user_id=user_id,
                user_name=user_name,
                role=role,
                is_attending=member.is_attending if member else None,
            )

            member.update_info(
                intent=intent,
                user_content=user_content,
            )
            self.member_repo.save(member)
            self.logger.info("Register Member process finished.")

        except Exception as e:
            raise RuntimeError(f"Failed to register member {user_id}") from e
