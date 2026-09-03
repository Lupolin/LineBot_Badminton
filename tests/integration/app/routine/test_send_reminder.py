from logging import Logger
from unittest.mock import Mock, call

import pytest

from app.routine import SendReminderUseCase
from domain.gateway import DateTimeCalendarService
from domain.repository import MemberProfileRepository
from domain.service import MessageGenerator
from tests.mock_data import PENDING_MEMBERS


@pytest.mark.asyncio
async def test_send_reminder_use_case(
    member_profile_repo: MemberProfileRepository,
    line_message_service_mock: Mock,
    message_generator: MessageGenerator,
    datetime_calendar_service: DateTimeCalendarService,
    logger: Logger,
):
    pending_members = PENDING_MEMBERS

    for member in pending_members:
        await member_profile_repo.save(member=member)

    use_case = SendReminderUseCase(
        member_profile_repo=member_profile_repo,
        message_service=line_message_service_mock,
        message_generator=message_generator,
        calendar=datetime_calendar_service,
        logger=logger,
    )

    await use_case.execute()

    played_date = datetime_calendar_service.get_played_date()
    today_name = datetime_calendar_service.get_today_name()
    get_pending_members = await member_profile_repo.get_pending_members()

    reminder_message = message_generator.get_reminder_message(
        played_date=played_date,
        today_name=today_name,
    )

    assert len(get_pending_members) == len(pending_members)

    expected_calls = [call(user_id=m.user_id, message=reminder_message) for m in pending_members]
    line_message_service_mock.push_message.assert_has_calls(expected_calls, any_order=False)
