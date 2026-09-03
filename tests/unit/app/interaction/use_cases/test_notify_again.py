from unittest.mock import call

import pytest

from app.interaction.use_cases import NotifyAgainUseCase
from domain.entity import (
    UserIntent,
)
from tests.mock_data import PENDING_MEMBERS, make_test_member, make_use_case_command


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
    test_member = make_test_member()
    test_member.user_content = "發出召集令"
    test_command = make_use_case_command()
    test_command.user_content = test_member.user_content
    test_command.intent = UserIntent.NOTIFY_AGAIN
    test_command.member = test_member

    result = await notify_again_use_case.execute(cmd=test_command)

    datetime_calendar_service_mock.get_played_date.assert_called_once_with()
    datetime_calendar_service_mock.get_today_name.assert_called_once_with()
    member_profile_repo_mock.get_pending_members.assert_awaited_once_with()
    member_profile_repo_mock.save.assert_awaited_once_with(member=test_command.member)

    played_date = datetime_calendar_service_mock.get_played_date.return_value
    today_name = datetime_calendar_service_mock.get_today_name.return_value
    reminder_message = message_generator.get_reminder_message(
        played_date=played_date,
        today_name=today_name,
    )

    pending_members = member_profile_repo_mock.get_pending_members.return_value
    expected_calls = [call(user_id=m.user_id, message=reminder_message) for m in pending_members]
    line_message_service_mock.push_message.assert_has_awaits(expected_calls, any_order=True)
    assert line_message_service_mock.push_message.call_count == len(PENDING_MEMBERS)

    assert result == "Handle notify process successful"
