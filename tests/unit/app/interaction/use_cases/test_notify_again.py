from unittest.mock import call

import pytest

from app.interaction.dispatcher import UseCaseCommand
from app.interaction.use_cases import NotifyAgainUseCase
from domain.entity import (
    MemberInfo,
    UserIntent,
)
from tests.mock_data import PENDING_MEMBERS_LIST


@pytest.fixture
def notify_again_use_case(
    member_profile_repo_mock,
    line_message_service_mock,
    message_generator,
    datetime_calendar_service_mock,
    logger,
):
    return NotifyAgainUseCase(
        member_profile_repo=member_profile_repo_mock,
        message_service=line_message_service_mock,
        message_generator=message_generator,
        calendar=datetime_calendar_service_mock,
        logger=logger,
    )


@pytest.mark.asyncio
async def test_notify_again_success(
    notify_again_use_case,
    member_profile_repo_mock,
    line_message_service_mock,
    message_generator,
    datetime_calendar_service_mock,
    logger,
):
    test_command = UseCaseCommand(
        user_id="U001",
        user_content="發出召集令",
        intent=UserIntent.NOTIFY_AGAIN,
        member=MemberInfo(
            user_id="U001",
            user_name="Lucas",
            user_content="發出召集令",
            role="Member",
            is_attending=None,
        ),
        reply_token="fake_token",
    )

    result = await notify_again_use_case.execute(test_command)

    datetime_calendar_service_mock.get_played_date.assert_called_once_with()
    datetime_calendar_service_mock.get_today_name.assert_called_once_with()
    member_profile_repo_mock.get_pending_members.assert_awaited_once_with()
    member_profile_repo_mock.save.assert_awaited_once_with(test_command.member)

    played_date = datetime_calendar_service_mock.get_played_date.return_value
    today_name = datetime_calendar_service_mock.get_today_name.return_value
    remind_message = message_generator.get_reminder_message(
        played_date=played_date,
        today_name=today_name,
    )

    pending_members = member_profile_repo_mock.get_pending_members.return_value
    expected_calls = [call(m.user_id, remind_message) for m in pending_members]
    line_message_service_mock.push_message.assert_has_awaits(expected_calls, any_order=True)
    assert line_message_service_mock.push_message.call_count == len(PENDING_MEMBERS_LIST)

    assert result == "Handle notify process successful"
