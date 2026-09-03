from logging import Logger

import pytest

from app.routine import FindAttendanceRecordUseCase
from domain.repository import AttendanceRecordRepository
from tests.mock_data import ALL_ATTENDANCE


@pytest.mark.asyncio
async def test_find_attendance_record_use_case(
    attendance_record_repo: AttendanceRecordRepository,
    logger: Logger,
):
    test_record = ALL_ATTENDANCE
    await attendance_record_repo.save_all(records=test_record)

    use_case = FindAttendanceRecordUseCase(
        attendance_record_repo=attendance_record_repo,
        logger=logger,
    )

    result = await use_case.execute()

    sorted_result = sorted(result, key=lambda x: x.user_id)
    sorted_expect = sorted(ALL_ATTENDANCE, key=lambda x: x.user_id)

    assert sorted_result == sorted_expect
