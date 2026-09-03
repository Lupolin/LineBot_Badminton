from logging import Logger

import pytest

from app.interaction.use_cases import HandleAttendanceUseCase
from domain.repository import MemberProfileRepository
from tests.mock_data import make_test_member, make_use_case_command


@pytest.mark.asyncio
async def test_handle_attendance_use_case(
    member_profile_repo: MemberProfileRepository,
    logger: Logger,
):
    test_member = make_test_member()
    test_member.user_content = "-1"
    test_command = make_use_case_command()
    test_command.member = test_member

    await member_profile_repo.save(member=test_member)

    use_case = HandleAttendanceUseCase(
        member_profile_repo=member_profile_repo,
        logger=logger,
    )

    result = await use_case.execute(cmd=test_command)

    get_test_member = await member_profile_repo.find_by_id(user_id=test_member.user_id)

    assert get_test_member is not None
    assert get_test_member.is_attending is True
    assert result == "Handle attendance process successful"
