from domain.routine.entities import BadmintonMessages, Member
from infrastructure.opentelemetry import trace_method
from infrastructure.setting.config import config


class MessageService:
    def __init__(
        self,
        messages: BadmintonMessages,
        timezone: str,
    ):
        self.msgs = messages
        self.tz = timezone

    @trace_method("Service: MessageService.get_reminder_message")
    def get_reminder_message(
        self,
        played_date: str,
        today_name: str,
    ) -> str:
        if today_name == "tuesday":
            template = self.msgs.ASK_TUESDAY
        elif today_name == "wednesday":
            template = self.msgs.ASK_WEDNESDAY
        else:
            template = self.msgs.ASK_DEFAULT

        return template.format(
            date=played_date,
            time=config.MESSAGE.TIME,
            location=config.MESSAGE.LOCATION,
        )

    @trace_method("Service: MessageService.get_summary_message")
    def get_summary_message(
        self,
        played_date: str,
        attending_members: list[Member],
        not_attending_members: list[Member],
        pending_members: list[Member],
    ) -> str:
        attending_str = self._format_member_list(attending_members)
        not_attending_str = self._format_member_list(not_attending_members)
        pending_str = self._format_member_list(pending_members)

        # 這裡會對應到您 messages.py 中的 SUMMARY_TEMPLATE
        return self.msgs.SUMMARY_TEMPLATE.format(
            date=played_date,
            attending_members=attending_str,
            not_attending_members=not_attending_str,
            pending_members=pending_str,
        )

    @staticmethod
    def _format_member_list(members: list[Member]) -> str:
        if not members:
            return "（無）"

        return "\n".join(f"- {member.user_name}" for member in members)
