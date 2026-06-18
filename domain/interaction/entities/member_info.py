from dataclasses import (
    dataclass,
    field,
)
from datetime import datetime

from .intent import UserIntent


@dataclass
class MemberInfo:
    user_id: str
    user_name: str
    user_content: str
    role: str = "Member"
    status: str | None = None
    intent: str | None = None
    is_attending: bool | None = None
    last_replied_at: datetime | None = field(default_factory=datetime.now)

    def update_attendance(self, intent: UserIntent, user_content: str):
        if intent == UserIntent.ATTEND:
            self.is_attending = True
        elif intent == UserIntent.CANCEL:
            self.is_attending = False

        self.update_info(
            intent=intent,
            user_content=user_content,
        )

    def update_info(self, intent: UserIntent, user_content: str):
        self.user_content = user_content
        self.intent = intent.name
        self._refresh_timestamp()

    def _refresh_timestamp(self):
        self.last_replied_at = datetime.now()
