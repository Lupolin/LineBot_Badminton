from dataclasses import dataclass
from logging import Logger

from domain.entity import (
    MemberInfo,
)
from domain.gateway import (
    MessagingApiClient,
    ProfileApiClient,
)
from domain.repository import MemberProfileRepository
from infrastructure.opentelemetry import trace_method

from ..dispatcher import UseCaseCommand


@dataclass
class RegisterMemberUseCase:
    member_profile_repo: MemberProfileRepository
    message_service: MessagingApiClient
    api_service: ProfileApiClient
    logger: Logger

    @trace_method("UseCase: RegisterMemberUseCase")
    async def execute(self, cmd: UseCaseCommand) -> str:
        self.logger.info(f"Executing RegisterMemberUseCase | User: {cmd.user_id} | Intent: {cmd.intent.name}")

        is_admin_request = cmd.user_content == "Admin"
        role = "Admin" if is_admin_request else "Member"
        message = "偷偷跟你說喔！你是我的管理員了❤️" if is_admin_request else "註冊好了！\n我再也不會忘記你了！"

        try:
            user_name = await self.api_service.get_user_name(user_id=cmd.user_id)

            member = MemberInfo(
                user_id=cmd.user_id,
                user_name=user_name,
                role=role,
                user_content=cmd.user_content,
                status="ACTIVE",
                is_attending=cmd.member.is_attending if cmd.member else None,
            )

            member.update_info(
                intent=cmd.intent,
                user_content=cmd.user_content,
            )

            await self.member_profile_repo.save(member=member)

            if cmd.reply_token:
                await self.message_service.reply_message(
                    reply_token=cmd.reply_token,
                    message=message,
                )

            self.logger.info(f"Register member process finished for user: {cmd.user_id}")
            return message

        except Exception as e:
            self.logger.error(
                f"UseCase Error [{type(e).__name__}]: Failed to handle register member for {cmd.user_id} - {str(e)}",
                exc_info=True,
            )
            return f"Failed to register member | UserId = {cmd.user_id}"
