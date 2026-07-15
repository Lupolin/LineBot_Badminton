import pytest

from app.routine import FindAttendanceRecordUseCase
from tests.mock_data import ALL_ATTENDANCE_LIST


@pytest.fixture
def find_attendance_record_use_case(
    attendance_record_repo_mock,
    logger,
):
    return FindAttendanceRecordUseCase(
        attendance_record_repo=attendance_record_repo_mock,
        logger=logger,
    )


@pytest.mark.asyncio
async def test_find_attendance_record_success(
    find_attendance_record_use_case,
    attendance_record_repo_mock,
    logger,
):
    result = await find_attendance_record_use_case.execute()
    attendance_record_repo_mock.find_all_data.assert_awaited_once_with()

    assert result == ALL_ATTENDANCE_LIST
