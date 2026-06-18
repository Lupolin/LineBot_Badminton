from fastapi import APIRouter

from .find_attendance_record import find_attendance_record
from .find_top_absentees import find_top_absentees
from .insert_attendance_record import insert_attendance_record
from .reset_attendance import reset_attendance
from .send_reminder import send_reminder
from .send_summary import send_summary
from .update_played_date import update_played_date

router = APIRouter(
    prefix="/routine",
    tags=["Routine"],
)

router.add_api_route(
    "/SendReminder",
    send_reminder,
    methods=["POST"],
    summary="發送羽球催促提醒",
)

router.add_api_route(
    "/SendSummary",
    send_summary,
    methods=["POST"],
    summary="發送出席統計",
)

router.add_api_route(
    "/ResetAttendance",
    reset_attendance,
    methods=["POST"],
    summary="手動重置出席狀態",
)

router.add_api_route(
    "/UpdatePlayedDate",
    update_played_date,
    methods=["POST"],
    summary="更新已打球日期",
)

router.add_api_route(
    "/InsertAttendanceRecord",
    insert_attendance_record,
    methods=["POST"],
    summary="同步成員出席紀錄",
)

router.add_api_route(
    "/FindTopAbsentees",
    find_top_absentees,
    methods=["POST"],
    summary="獲取請假最多次前三名",
)

router.add_api_route(
    "/FindAttendanceRecord",
    find_attendance_record,
    methods=["POST"],
    summary="獲取全部出席紀錄",
)
