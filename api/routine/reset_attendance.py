from app.registry import registry
from infrastructure.response.schemas import ApiResponse


async def reset_attendance():
    use_case = registry.reset_attendance_use_case
    await use_case.execute()
    return ApiResponse.success_response(data=True)
