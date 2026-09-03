from dataclasses import dataclass

from domain.entity import (
    Absentee,
    BadmintonMessages,
    MemberInfo,
)
from infrastructure.opentelemetry import trace_method
from infrastructure.setting import config


@dataclass
class MessageGenerator:
    messages: BadmintonMessages

    @trace_method("Service: MessagingApiClient.get_reminder_message")
    def get_reminder_message(
        self,
        played_date: str,
        today_name: str,
    ) -> str:
        if today_name == "tuesday":
            template = self.messages.ASK_TUESDAY
        elif today_name == "wednesday":
            template = self.messages.ASK_WEDNESDAY
        else:
            template = self.messages.ASK_DEFAULT

        return template.format(
            date=played_date,
            time=config.MESSAGE.TIME,
            location=config.MESSAGE.LOCATION,
        )

    @trace_method("Service: MessageGenerator.get_summary_message")
    def get_summary_message(
        self,
        played_date: str,
        attending_members: list[MemberInfo],
        not_attending_members: list[MemberInfo],
        pending_members: list[MemberInfo],
    ) -> str:
        attending_str = self._format_member_list(attending_members)
        not_attending_str = self._format_member_list(not_attending_members)
        pending_str = self._format_member_list(pending_members)

        # 這裡會對應到您 messages.py 中的 SUMMARY_TEMPLATE
        return self.messages.SUMMARY_TEMPLATE.format(
            date=played_date,
            attending_members=attending_str,
            not_attending_members=not_attending_str,
            pending_members=pending_str,
        )

    @trace_method("Service: MessageGenerator.get_attendance_result_message")
    def get_attendance_result_message(
        self,
        absentee: list[Absentee],
    ) -> str:
        if not absentee:
            return "目前沒有請假王喔！大家都好乖～"

        display_data = {"champion": "從缺", "runner_up": "從缺", "second_runner_up": "從缺"}

        keys = ["champion", "runner_up", "second_runner_up"]

        for i, person in enumerate(absentee[:3]):
            display_data[keys[i]] = f"{person.user_name} (請假：{person.absent_count}次)"

        return self.messages.TOP_ABSENTEES_TEMPLATE.format(**display_data)

    @staticmethod
    def _format_member_list(members: list[MemberInfo]) -> str:
        if not members:
            return "（無）"

        return "\n".join(f"- {member.user_name}" for member in members)
