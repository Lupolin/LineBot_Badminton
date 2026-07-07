import pytest

from app.interaction.dispatcher import UseCaseCommand
from app.interaction.usecases import SendTopAbsenteeUseCase
from domain.entity import (
    MemberInfo,
    UserIntent,
)


@pytest.fixture
def send_top_absentee_use_case(
    member_profile_repo_mock,
    attendance_record_repo_mock,
    line_message_service_mock,
    message_generator,
    logger,
):
    return SendTopAbsenteeUseCase(
        member_profile_repo=member_profile_repo_mock,
        absentee_repo=attendance_record_repo_mock,
        message_service=line_message_service_mock,
        message_generator=message_generator,
        logger=logger,
    )


@pytest.mark.asyncio
async def test_send_top_absentee_success(
    send_top_absentee_use_case,
    attendance_record_repo_mock,
    member_profile_repo_mock,
    line_message_service_mock,
    message_generator,
    logger,
):
    test_command = UseCaseCommand(
        user_id="U001",
        user_content="誰是請假王",
        intent=UserIntent.NOTIFY_AGAIN,
        member=MemberInfo(
            user_id="U001",
            user_name="Lucas",
            user_content="誰是請假王",
            role="Member",
            is_attending=None,
        ),
        reply_token="fake_token",
    )

    result = await send_top_absentee_use_case.execute(test_command)

    attendance_record_repo_mock.find_top_absentees.assert_awaited_once_with()
    member_profile_repo_mock.save.assert_awaited_once_with(test_command.member)

    raw_list = attendance_record_repo_mock.find_top_absentees.return_value
    top_absentee_list = raw_list if raw_list is not None else []
    top_absentee_message = message_generator.get_attendance_result_message(absentee=top_absentee_list)

    line_message_service_mock.reply_message.assert_called_once_with(
        reply_token=test_command.reply_token,
        message=top_absentee_message,
    )

    assert result == top_absentee_message
