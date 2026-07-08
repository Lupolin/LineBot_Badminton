from datetime import datetime

from domain.entity import (
    Absentee,
    Admin,
    Attendance,
    MemberInfo,
    MessageEvent,
)

MESSAGE_EVENT: MessageEvent = MessageEvent(
    user_id="Lucas",
    user_content="註冊",
    reply_token="Fake_Token",
)

ALL_ATTENDANCE_LIST: list[Attendance] = [
    Attendance(user_id="U001", user_name="Lucas", is_attending=False, played_date="07/03"),
    Attendance(user_id="U002", user_name="Amy", is_attending=False, played_date="07/03"),
    Attendance(user_id="U003", user_name="Andy", is_attending=True, played_date="07/03"),
]

TOP_ABSENTEES_LIST: list[Absentee] = [
    Absentee(user_name="Lucas", absent_count=3),
    Absentee(user_name="Amy", absent_count=5),
    Absentee(user_name="Andy", absent_count=2),
]

PENDING_MEMBERS_LIST: list[MemberInfo] = [
    MemberInfo(user_id="U001", user_name="Lucas", user_content="統計", is_attending=None),
    MemberInfo(user_id="U002", user_name="Amy", user_content="註冊", is_attending=None),
]


ATTENDING_MEMBERS_LIST: list[MemberInfo] = [
    MemberInfo(user_id="U003", user_name="Andy", user_content="+1", is_attending=True),
    MemberInfo(user_id="U004", user_name="Mars", user_content="+1", is_attending=True),
]

NOT_ATTENDING_MEMBERS_LIST: list[MemberInfo] = [
    MemberInfo(user_id="U005", user_name="Lisa", user_content="-1", is_attending=False),
    MemberInfo(user_id="U006", user_name="Hank", user_content="-1", is_attending=False),
]

ADMIN_MEMBERS_LIST: list[Admin] = [
    Admin(user_id="U001", user_role="Admin"),
    Admin(user_id="U002", user_role="Admin"),
    Admin(user_id="U003", user_role="Admin"),
]

FIND_BY_ID: MemberInfo = MemberInfo(
    user_id="U001",
    user_name="Lucas",
    user_content="",
    role="Member",
    status="ACTIVE",
    is_attending=True,
    intent="QUERY_STAT",
    last_replied_at=datetime(2026, 7, 2, 10, 30, 0),
)
