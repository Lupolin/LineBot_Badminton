from __future__ import annotations

from dataclasses import dataclass
from logging import Logger
from typing import TYPE_CHECKING

from domain.entity import MemberInfo, UserIntent
from domain.gateway import MessageService
from domain.repository import MemberProfileRepository
from infrastructure.opentelemetry import trace_method

if TYPE_CHECKING:
    from app.registry import Registry


@dataclass
class IntentDispatcherCommand:
    user_id: str
    user_content: str
    reply_token: str | None = None


@dataclass
class UseCaseCommand:
    user_id: str
    user_content: str
    intent: UserIntent
    member: MemberInfo | None
    reply_token: str | None = None


@dataclass
class IntentDispatcher:
    registry: Registry
    member_profile_repo: MemberProfileRepository
    message_service: MessageService
    logger: Logger

    @trace_method("UseCase: IntentDispatcher.execute")
    async def execute(self, cmd: IntentDispatcherCommand) -> str:
        intent = UserIntent.from_text(cmd.user_content)
        member = await self.member_profile_repo.find_by_id(cmd.user_id)

        self.logger.info(f"Dispatching request | User: {cmd.user_id} | Intent: {intent.name}")

        if not member and intent != UserIntent.REGISTER:
            message = "你...你是誰啊？！\n你不在註冊名單內啊！"
            if cmd.reply_token:
                await self.message_service.reply_message(
                    reply_token=cmd.reply_token,
                    message=message,
                )
            self.logger.error(f"User: {cmd.user_id} not found.")
            return message

        if intent == UserIntent.UNKNOWN:
            self.logger.error("Unknown intent")
            return "Unknown intent"

        self.logger.info(f"Dispatching message: user={cmd.user_id}, intent={intent.name}")

        use_case = self.registry.get_use_case_by_intent(intent)
        if use_case is None:
            self.logger.error(f"No UseCase found for intent={intent.name}, content='{cmd.user_content}'")
            return "No UseCase found for your request."

        if member:
            member.update_info(
                intent=intent,
                user_content=cmd.user_content,
            )

        message = await use_case.execute(
            UseCaseCommand(
                user_id=cmd.user_id,
                user_content=cmd.user_content,
                intent=intent,
                member=member,
                reply_token=cmd.reply_token,
            )
        )

        return message
