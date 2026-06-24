from dataclasses import dataclass
from logging import Logger

from domain.entity import (
    MemberInfo,
    UserIntent,
)
from domain.gateway import (
    ApiService,
    MessageService,
)
from domain.repository import MemberProfileRepository
from infrastructure.opentelemetry import trace_method


@dataclass
class RegisterMemberUseCase:
    member_profile_repo: MemberProfileRepository
    message_service: MessageService
    api_service: ApiService
    logger: Logger

    @trace_method("UseCase: RegisterMemberUseCase")
    async def execute(
        self,
        user_id: str,
        user_content: str,
        reply_token: str,
        intent: UserIntent,
        member: MemberInfo,
    ) -> str:
        self.logger.info(f"Executing RegisterMemberUseCase | User: {user_id} | Intent: {intent.name}")

        is_admin_request = user_content == "Admin"
        role = "Admin" if is_admin_request else "Member"
        message = "偷偷跟你說喔！你是我的管理員了❤️" if is_admin_request else "註冊好了！\n我再也不會忘記你了！"

        try:
            user_name = await self.api_service.get_user_name(user_id)

            member = MemberInfo(
                user_id=user_id,
                user_name=user_name,
                role=role,
                user_content=user_content,
                status="ACTIVE",
                is_attending=member.is_attending if member else None,
            )

            member.update_info(
                intent=intent,
                user_content=user_content,
            )

            await self.member_profile_repo.save(member)

            if reply_token:
                await self.message_service.reply_message(
                    reply_token=reply_token,
                    message=message,
                )

            self.logger.info(f"Register member process finished for user: {user_id}")
            return message

        except Exception as e:
            self.logger.error(
                f"UseCase Error [{type(e).__name__}]: Failed to handle register member for {user_id} - {str(e)}",
                exc_info=True,
            )
            return f"Failed to register member | UserId = {user_id}"
