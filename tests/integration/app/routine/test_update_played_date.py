from logging import Logger

import pytest

from app.routine import UpdatePlayedDateUseCase
from domain.gateway import DateTimeCalendarService
from domain.repository import AttendanceRecordRepository, MemberProfileRepository
from tests.mock_data import MEMBER_PROFILE_DATA


@pytest.mark.asyncio
async def test_update_played_date_use_case(
    member_profile_repo: MemberProfileRepository,
    attendance_record_repo: AttendanceRecordRepository,
    datetime_calendar_service: DateTimeCalendarService,
    logger: Logger,
):
    member_profile_data = MEMBER_PROFILE_DATA

    for member in member_profile_data:
        await member_profile_repo.save(member=member)

    use_case = UpdatePlayedDateUseCase(
        member_profile_repo=member_profile_repo,
        calendar=datetime_calendar_service,
        logger=logger,
    )

    await use_case.execute()

    played_date = datetime_calendar_service.get_played_date()
    attendance_records = await attendance_record_repo.get_all_data()

    for record in attendance_records:
        assert record.played_date == played_date
