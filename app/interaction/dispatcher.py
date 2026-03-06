from domain.interaction.entities import UserIntent
from domain.interaction.repository import UpdateMemberInfoRepository
from infrastructure.common import LineMessageService
from infrastructure.opentelemetry import trace_method


class IntentDispatcher:
    def __init__(
        self,
        registry,
        member_repo: UpdateMemberInfoRepository,
        messenger: LineMessageService,
    ):
        self._registry = registry
        self.member_repo = member_repo
        self.messenger = messenger

    @trace_method("UseCase: IntentDispatcher.execute")
    def execute(self, user_id: str, user_content: str) -> None:
        intent = UserIntent.from_text(user_content)
        member = self.member_repo.find_by_id(user_id)

        if not member and intent != UserIntent.REGISTER:
            self.messenger.push_message(
                user_id=user_id,
                message="你...你是誰啊？！\n你不在註冊名單內啊！",
            )
            raise ValueError(f"User {user_id} not found.")

        if intent == UserIntent.UNKNOWN:
            return

        self._registry.logger.info(f"Dispatching message: user={user_id}, intent={intent.name}")

        use_case = self._registry.get_use_case_by_intent(intent)

        if use_case is None:
            raise ValueError(f"No UseCase found for intent={intent.name}, content='{user_content}'")

        use_case.execute(
            user_id=user_id,
            user_content=user_content,
            intent=intent,
            member=member,
        )
