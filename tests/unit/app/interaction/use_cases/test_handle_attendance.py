import pytest

from app.interaction.use_cases import HandleAttendanceUseCase
from domain.entity import (
    UserIntent,
)
from tests.mock_data import make_test_member, make_use_case_command


@pytest.fixture
def handle_attendance_use_case(member_profile_repo_mock, logger):
    return HandleAttendanceUseCase(
        member_profile_repo=member_profile_repo_mock,
        logger=logger,
    )


@pytest.mark.asyncio
async def test_handle_attendance_success(
    handle_attendance_use_case,
    member_profile_repo_mock,
    logger,
):
    test_member = make_test_member()
    test_member.user_content = "+1"
    test_command = make_use_case_command()
    test_command.user_content = test_member.user_content
    test_command.intent = UserIntent.ATTEND
    test_command.member = test_member

    result = await handle_attendance_use_case.execute(cmd=test_command)

    member_profile_repo_mock.save.assert_awaited_once()
    actual_member = member_profile_repo_mock.save.call_args.kwargs["member"]
    assert actual_member.is_attending is True

    assert result == "Handle attendance process successful"
