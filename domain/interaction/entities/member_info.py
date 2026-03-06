from dataclasses import dataclass
from datetime import datetime

from .intent import UserIntent


@dataclass
class MemberInfo:
    user_id: str
    user_name: str
    role: str = "Member"
    intent: str | None = None
    is_attending: bool | None = None
    user_content: str | None = None
    last_replied_at: datetime = datetime.now()

    def update_attendance(self, intent: UserIntent, user_content: str):
        if intent == UserIntent.ATTEND:
            self.is_attending = True
        elif intent == UserIntent.CANCEL:
            self.is_attending = False

        self.update_info(intent=intent, user_content=user_content)

    def update_info(self, intent: UserIntent, user_content: str):
        self.user_content = user_content
        self.intent = intent.name
        self._refresh_timestamp()

    def _refresh_timestamp(self):
        self.last_replied_at = datetime.now()
