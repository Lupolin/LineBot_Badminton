from app import registry
from infrastructure.response.schemas import ApiResponse


async def find_attendance_record():
    use_case = registry.find_attendance_record_use_case
    data = await use_case.execute()
    return ApiResponse.success_response(data=data)
