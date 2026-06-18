from app.registry import registry
from infrastructure.response.schemas import ApiResponse


async def send_summary():
    use_case = registry.send_summary_use_case
    await use_case.execute()
    return ApiResponse.success_response(data=True)
