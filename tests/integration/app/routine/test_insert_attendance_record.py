from logging import Logger

import pytest

from app.routine import InsertAttendanceRecordUseCase
from domain.repository import AttendanceRecordRepository, MemberProfileRepository
from tests.mock_data import MEMBER_PROFILE_DATA


@pytest.mark.asyncio
async def test_insert_attendance_record_use_case(
    member_profile_repo: MemberProfileRepository,
    attendance_record_repo: AttendanceRecordRepository,
    logger: Logger,
):
    member_profile_data = MEMBER_PROFILE_DATA

    for member in member_profile_data:
        await member_profile_repo.save(member=member)

    use_case = InsertAttendanceRecordUseCase(
        attendance_record_repo=attendance_record_repo,
        logger=logger,
    )

    await use_case.execute()

    result = await attendance_record_repo.find_all_data()

    assert result is not None
    assert len(result) == len(member_profile_data)
