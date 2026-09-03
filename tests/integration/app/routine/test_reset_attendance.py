from logging import Logger

import pytest

from app.routine import ResetAttendanceUseCase
from domain.repository import MemberProfileRepository
from tests.mock_data import MEMBER_PROFILE_DATA


@pytest.mark.asyncio
async def test_reset_attendance_use_case(
    member_profile_repo: MemberProfileRepository,
    logger: Logger,
):
    member_profile_data = MEMBER_PROFILE_DATA

    for member in member_profile_data:
        await member_profile_repo.save(member=member)

    use_case = ResetAttendanceUseCase(
        member_profile_repo=member_profile_repo,
        logger=logger,
    )

    await use_case.execute()

    get_pending_members = await member_profile_repo.get_pending_members()
    get_attending_members = await member_profile_repo.get_attending_members()
    get_not_attending_members = await member_profile_repo.get_not_attending_members()

    assert len(get_pending_members) == len(member_profile_data)
    assert not get_attending_members
    assert not get_not_attending_members

    for member in get_pending_members:
        assert member.is_attending is None
        assert member.played_date is None
