from logging import Logger

import pytest

from app.routine import FindTopAbsenteesUseCase
from domain.repository import AttendanceRecordRepository
from tests.mock_data import TOP_ABSENTEES, TOP_ABSENTEES_DATA


@pytest.mark.asyncio
async def test_find_attendance_record_use_case(
    attendance_record_repo: AttendanceRecordRepository,
    logger: Logger,
):
    test_record = TOP_ABSENTEES_DATA
    await attendance_record_repo.save_all(records=test_record)

    use_case = FindTopAbsenteesUseCase(
        attendance_record_repo=attendance_record_repo,
        logger=logger,
    )

    result = await use_case.execute()

    sorted_result = sorted(result, key=lambda x: x.absent_count, reverse=True)
    sorted_expect = sorted(TOP_ABSENTEES, key=lambda x: x.absent_count, reverse=True)

    assert sorted_result == sorted_expect
