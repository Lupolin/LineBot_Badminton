from app.registry import registry
from infrastructure.response.schemas import ApiResponse


async def update_played_date():
    use_case = registry.update_played_date_use_case
    await use_case.execute()
    return ApiResponse.success_response(data=True)
