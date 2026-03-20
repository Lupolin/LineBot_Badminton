from logging import Logger

from domain.interaction.entities import (
    MemberInfo,
    UserIntent,
)
from domain.interaction.repository import UpdateMemberInfoRepository
from infrastructure.common import LineMessageService
from infrastructure.opentelemetry import trace_method


class RegisterMemberUseCase:
    def __init__(
        self,
        member_repo: UpdateMemberInfoRepository,
        messenger: LineMessageService,
        line_api_service,
        logger: Logger,
    ):
        self.member_repo = member_repo
        self.messenger = messenger
        self.line_api_service = line_api_service
        self.logger = logger

    @trace_method("UseCase: RegisterMemberUseCase")
    def execute(
        self,
        user_id: str,
        user_content: str,
        reply_token: str,
        intent: UserIntent,
        member: MemberInfo,
    ) -> None:
        self.logger.info(f"RegisterMemberUseCase: user_id={user_id}, intent={intent}")

        is_admin_request = user_content == "註冊Admin"
        role = "Admin" if is_admin_request else "Member"
        message = "偷偷跟你說喔！你是我的管理員了❤️" if is_admin_request else "註冊好了！\n我再也不會忘記你了！"

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
            if reply_token:
                self.messenger.reply_message(
                    reply_token=reply_token,
                    message=message,
                )
            else:
                self.messenger.push_message(
                    user_id=user_id,
                    message=message,
                )
            self.logger.info("Register Member process finished.")

        except Exception as e:
            raise RuntimeError(f"Failed to register member {user_id}") from e
