from unittest.mock import call

import pytest

from app.routine import SendSummaryUseCase
from tests.unit.mock_data import ADMIN_MEMBERS_LIST


@pytest.fixture
def send_summary_use_case(
    member_profile_repo_mock,
    line_message_service_mock,
    message_generator,
    datetime_calendar_service_mock,
    logger,
):
    return SendSummaryUseCase(
        member_profile_repo=member_profile_repo_mock,
        message_service=line_message_service_mock,
        message_generator=message_generator,
        calendar=datetime_calendar_service_mock,
        logger=logger,
    )


@pytest.mark.asyncio
async def test_send_summary_success(
    send_summary_use_case,
    member_profile_repo_mock,
    line_message_service_mock,
    message_generator,
    datetime_calendar_service_mock,
    logger,
):
    await send_summary_use_case.execute()

    datetime_calendar_service_mock.get_played_date.assert_called_once_with()
    member_profile_repo_mock.get_admin_members.assert_called_once()
    member_profile_repo_mock.get_attending_members.assert_called_once()
    member_profile_repo_mock.get_not_attending_members.assert_called_once()
    member_profile_repo_mock.get_pending_members.assert_called_once()

    played_date = datetime_calendar_service_mock.get_played_date.return_value
    admin_members = member_profile_repo_mock.get_admin_members.return_value
    attending_members = member_profile_repo_mock.get_attending_members.return_value
    not_attending_members = member_profile_repo_mock.get_not_attending_members.return_value
    pending_members = member_profile_repo_mock.get_pending_members.return_value

    summary_message = message_generator.get_summary_message(
        played_date=played_date,
        attending_members=attending_members,
        not_attending_members=not_attending_members,
        pending_members=pending_members,
    )

    expected_calls = [call(m.user_id, summary_message) for m in admin_members]
    line_message_service_mock.push_message.assert_has_awaits(expected_calls, any_order=True)
    assert line_message_service_mock.push_message.call_count == len(ADMIN_MEMBERS_LIST)
