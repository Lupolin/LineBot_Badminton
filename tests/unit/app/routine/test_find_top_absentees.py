import pytest

from app.routine import FindTopAbsenteesUseCase
from tests.mock_data import TOP_ABSENTEES


@pytest.fixture
def find_top_absentees_use_case(
    attendance_record_repo_mock,
    logger,
):
    return FindTopAbsenteesUseCase(
        attendance_record_repo=attendance_record_repo_mock,
        logger=logger,
    )


@pytest.mark.asyncio
async def test_find_top_absentees_success(
    find_top_absentees_use_case,
    attendance_record_repo_mock,
    logger,
):
    result = await find_top_absentees_use_case.execute()
    attendance_record_repo_mock.find_top_absentees.assert_awaited_once_with()

    assert result == TOP_ABSENTEES
