import pytest

from app.routine import InsertAttendanceRecordUseCase


@pytest.fixture
def insert_attendance_record_use_case(
    attendance_record_repo_mock,
    logger,
):
    return InsertAttendanceRecordUseCase(
        attendance_record_repo=attendance_record_repo_mock,
        logger=logger,
    )


@pytest.mark.asyncio
async def test_insert_attendance_record_success(
    insert_attendance_record_use_case,
    attendance_record_repo_mock,
    logger,
):
    await insert_attendance_record_use_case.execute()

    records = attendance_record_repo_mock.get_all_data.return_value
    attendance_record_repo_mock.get_all_data.assert_awaited_once_with()
    attendance_record_repo_mock.save_all.assert_awaited_once_with(records=records)
