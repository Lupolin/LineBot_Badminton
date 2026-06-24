from app import registry
from infrastructure.response.schemas import ApiResponse


async def insert_attendance_record():
    use_case = registry.insert_attendance_record_use_case
    await use_case.execute()
    return ApiResponse.success_response(data=True)
