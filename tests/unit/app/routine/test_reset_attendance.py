import pytest

from app.routine import ResetAttendanceUseCase


@pytest.fixture
def reset_attendance_use_case(
    member_profile_repo_mock,
    logger,
):
    return ResetAttendanceUseCase(
        member_profile_repo=member_profile_repo_mock,
        logger=logger,
    )


@pytest.mark.asyncio
async def test_reset_attendance_success(
    reset_attendance_use_case,
    member_profile_repo_mock,
    logger,
):
    await reset_attendance_use_case.execute()
    member_profile_repo_mock.reset_all_attendance.assert_awaited_once_with()
