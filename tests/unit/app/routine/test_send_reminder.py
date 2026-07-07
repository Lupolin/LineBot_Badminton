from unittest.mock import call

import pytest

from app.routine import SendReminderUseCase
from tests.unit.mock_data import PENDING_MEMBERS_LIST


@pytest.fixture
def send_reminder_use_case(
    member_profile_repo_mock,
    line_message_service_mock,
    message_generator,
    datetime_calendar_service_mock,
    logger,
):
    return SendReminderUseCase(
        member_profile_repo=member_profile_repo_mock,
        message_service=line_message_service_mock,
        message_generator=message_generator,
        calendar=datetime_calendar_service_mock,
        logger=logger,
    )


@pytest.mark.asyncio
async def test_send_reminder_success(
    send_reminder_use_case,
    member_profile_repo_mock,
    line_message_service_mock,
    message_generator,
    datetime_calendar_service_mock,
    logger,
):
    await send_reminder_use_case.execute()

    datetime_calendar_service_mock.get_played_date.assert_called_once_with()
    datetime_calendar_service_mock.get_today_name.assert_called_once_with()
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
