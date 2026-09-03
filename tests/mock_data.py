from datetime import datetime

from app.interaction.dispatcher import IntentDispatcherCommand, UseCaseCommand
from domain.entity import (
    Absentee,
    Admin,
    Attendance,
    MemberInfo,
    MessageEvent,
)
from domain.entity.intent import UserIntent

MESSAGE_EVENT: MessageEvent = MessageEvent(
    user_id="Lucas",
    user_content="註冊",
    reply_token="Fake_Token",
)

ALL_ATTENDANCE: list[Attendance] = [
    Attendance(user_id="U001", user_name="Lucas", is_attending=False, played_date="07/03"),
    Attendance(user_id="U002", user_name="Amy", is_attending=False, played_date="07/03"),
    Attendance(user_id="U003", user_name="Andy", is_attending=True, played_date="07/03"),
]

TOP_ABSENTEES: list[Absentee] = [
    Absentee(user_name="Lucas", absent_count=3),
    Absentee(user_name="Amy", absent_count=2),
    Absentee(user_name="Andy", absent_count=1),
]

TOP_ABSENTEES_DATA: list[Attendance] = [
    Attendance(user_id="U001", user_name="Lucas", is_attending=False, played_date="07/03"),
    Attendance(user_id="U001", user_name="Lucas", is_attending=False, played_date="07/10"),
    Attendance(user_id="U001", user_name="Lucas", is_attending=False, played_date="07/17"),
    Attendance(user_id="U002", user_name="Amy", is_attending=False, played_date="07/03"),
    Attendance(user_id="U002", user_name="Amy", is_attending=False, played_date="07/10"),
    Attendance(user_id="U003", user_name="Andy", is_attending=False, played_date="07/03"),
    Attendance(user_id="U004", user_name="Mars", is_attending=False, played_date="07/03"),
    Attendance(user_id="U005", user_name="Lisa", is_attending=False, played_date="07/03"),
]

PENDING_MEMBERS: list[MemberInfo] = [
    MemberInfo(
        user_id="U001",
        user_name="Lucas",
        user_content="統計",
        role="Member",
        status="ACTIVE",
        is_attending=None,
        intent="QUERY_STAT",
    ),
    MemberInfo(
        user_id="U002",
        user_name="Amy",
        user_content="註冊",
        role="Member",
        status="ACTIVE",
        is_attending=None,
        intent="REGISTER",
    ),
]


ATTENDING_MEMBERS: list[MemberInfo] = [
    MemberInfo(
        user_id="U003",
        user_name="Andy",
        user_content="+1",
        role="Member",
        status="ACTIVE",
        is_attending=True,
        intent="ATTEND",
    ),
    MemberInfo(
        user_id="U004",
        user_name="Mars",
        user_content="+1",
        role="Member",
        status="ACTIVE",
        is_attending=True,
        intent="ATTEND",
    ),
]

NOT_ATTENDING_MEMBERS: list[MemberInfo] = [
    MemberInfo(
        user_id="U005",
        user_name="Lisa",
        user_content="-1",
        role="Member",
        status="ACTIVE",
        is_attending=False,
        intent="NOT_ATTEND",
    ),
    MemberInfo(
        user_id="U006",
        user_name="Hank",
        user_content="-1",
        role="Member",
        status="ACTIVE",
        is_attending=False,
        intent="NOT_ATTEND",
    ),
]

ADMIN_MEMBERS: list[Admin] = [
    Admin(user_id="U001", user_role="Admin"),
    Admin(user_id="U002", user_role="Admin"),
    Admin(user_id="U003", user_role="Admin"),
]

MEMBER_PROFILE_DATA: list[MemberInfo] = [
    *PENDING_MEMBERS,
    *ATTENDING_MEMBERS,
    *NOT_ATTENDING_MEMBERS,
]


def make_test_admin() -> MemberInfo:
    return MemberInfo(
        user_id="U002",
        user_name="Amy",
        user_content="Admin",
        role="Admin",
        status="ACTIVE",
        is_attending=None,
        intent="REGISTER",
        last_replied_at=datetime(2026, 7, 2, 10, 30, 0),
    )


def make_test_member() -> MemberInfo:
    return MemberInfo(
        user_id="U001",
        user_name="Lucas",
        user_content="+1",
        role="Member",
        status="ACTIVE",
        is_attending=True,
        intent="ATTEND",
        last_replied_at=datetime(2026, 7, 2, 10, 30, 0),
    )


def make_intent_dispatcher_command() -> IntentDispatcherCommand:
    return IntentDispatcherCommand(
        user_id="",
        user_content="",
        reply_token="fake_token",
    )


def make_use_case_command() -> UseCaseCommand:
    return UseCaseCommand(
        user_id="U001",
        user_content="+1",
        intent=UserIntent.ATTEND,
        member=None,
        reply_token="fake_token",
    )
