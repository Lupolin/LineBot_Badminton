from app import registry
from infrastructure.response.schemas import ApiResponse


async def find_top_absentees():
    use_case = registry.find_top_absentees_use_case
    data = await use_case.execute()
    return ApiResponse.success_response(data=data)
