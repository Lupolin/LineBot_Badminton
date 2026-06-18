from __future__ import annotations

from dataclasses import dataclass
from logging import Logger
from typing import TYPE_CHECKING

from domain.interaction.entities import UserIntent
from domain.interaction.repository import UpdateMemberInfoRepository
from infrastructure.common import LineMessageService
from infrastructure.opentelemetry import trace_method

if TYPE_CHECKING:
    from app.registry import Registry


@dataclass
class IntentDispatcher:
    registry: Registry
    member_repo: UpdateMemberInfoRepository
    messenger: LineMessageService
    logger: Logger

    @trace_method("UseCase: IntentDispatcher.execute")
    async def execute(
        self,
        user_id: str,
        user_content: str,
        reply_token: str | None = None,
    ) -> str:
        intent = UserIntent.from_text(user_content)
        member = await self.member_repo.find_by_id(user_id)

        self.logger.info(f"Dispatching request | User: {user_id} | Intent: {intent.name}")

        if not member and intent != UserIntent.REGISTER:
            message = "你...你是誰啊？！\n你不在註冊名單內啊！"
            if reply_token:
                await self.messenger.reply_message(
                    reply_token=reply_token,
                    message=message,
                )

            self.logger.error(f"User: {user_id} not found.")
            return message

        if intent == UserIntent.UNKNOWN:
            self.logger.error("Unknown intent")
            return "Unknown intent"

        self.logger.info(f"Dispatching message: user={user_id}, intent={intent.name}")

        use_case = self.registry.get_use_case_by_intent(intent)

        if use_case is None:
            self.logger.error(f"No UseCase found for intent={intent.name}, content='{user_content}'")
            return "No UseCase found for your request."

        message = await use_case.execute(
            user_id=user_id,
            user_content=user_content,
            reply_token=reply_token,
            intent=intent,
            member=member,
        )

        return message
