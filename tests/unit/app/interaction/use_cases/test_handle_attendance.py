import pytest

from app.interaction.dispatcher import UseCaseCommand
from app.interaction.usecases import HandleAttendanceUseCase
from domain.entity import (
    MemberInfo,
    UserIntent,
)


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
    test_command = UseCaseCommand(
        user_id="U001",
        user_content="+1",
        intent=UserIntent.ATTEND,
        member=MemberInfo(
            user_id="U001",
            user_name="Lucas",
            user_content="+1",
            role="Member",
            is_attending=None,
        ),
        reply_token="fake_token",
    )

    result = await handle_attendance_use_case.execute(test_command)

    assert test_command.member is not None
    assert test_command.member.is_attending is True
    member_profile_repo_mock.save.assert_awaited_once_with(test_command.member)

    assert result == "Handle attendance process successful"
