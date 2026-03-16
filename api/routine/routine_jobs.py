from fastapi import APIRouter, status

from app.registry import registry
from infrastructure.opentelemetry import trace_method
from infrastructure.response.schemas import ApiResponse

router = APIRouter()


@router.post(
    "/reminder",
    status_code=status.HTTP_200_OK,
    summary="發送羽球催促提醒",
    description="觸發 UseCase 執行催促尚未回覆成員的邏輯",
    response_model=ApiResponse[bool],
)
@trace_method("API: SendReminder")
def send_reminder():
    use_case = registry.send_reminder_use_case
    use_case.execute()
    return ApiResponse.success_response(data=True)


@router.post(
    "/summary",
    status_code=status.HTTP_200_OK,
    summary="發送出席統計",
    description="觸發 UseCase 執行發送出席統計給管理員的邏輯",
    response_model=ApiResponse[bool],
)
@trace_method("API: SendSummary")
def send_summary():
    use_case = registry.send_summary_use_case
    use_case.execute()
    return ApiResponse.success_response(data=True)


@router.post(
    "/reset-attendance",
    status_code=status.HTTP_200_OK,
    summary="手動重置出席狀態",
    description="觸發 UseCase 執行清空所有成員出席狀態與相關紀錄的邏輯",
    response_model=ApiResponse[bool],
)
@trace_method("API: ResetAttendance")
def reset_attendance():
    use_case = registry.reset_attendance_use_case
    use_case.execute()
    return ApiResponse.success_response(data=True)


@router.post(
    "/update-played-date",
    status_code=status.HTTP_200_OK,
    summary="更新已打球日期",
    description="觸發 UseCase 執行更新成員已打球日期的邏輯",
    response_model=ApiResponse[bool],
)
@trace_method("API: UpdatePlayedDate")
def update_played_date():
    use_case = registry.update_played_date_use_case
    use_case.execute()
    return ApiResponse.success_response(data=True)


@router.post(
    "/insert-attendance-record",
    status_code=status.HTTP_200_OK,
    summary="同步成員出席紀錄",
    description="觸發 UseCase 執行同步成員已出席紀錄的邏輯",
    response_model=ApiResponse[bool],
)
@trace_method("API: InsertAttendanceRecord")
def insert_attendance_record():
    use_case = registry.insert_attendance_record_use_case
    use_case.execute()
    return ApiResponse.success_response(data=True)
