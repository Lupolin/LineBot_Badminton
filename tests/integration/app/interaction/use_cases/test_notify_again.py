from logging import Logger
from unittest.mock import Mock, call

import pytest

from app.interaction.use_cases import NotifyAgainUseCase
from domain.entity import UserIntent
from domain.gateway import DateTimeCalendarService
from domain.repository import MemberProfileRepository
from domain.service import MessageGenerator
from tests.mock_data import PENDING_MEMBERS, make_test_member, make_use_case_command


@pytest.mark.asyncio
async def test_notify_again_use_case(
    member_profile_repo: MemberProfileRepository,
    line_message_service_mock: Mock,
    message_generator: MessageGenerator,
    datetime_calendar_service: DateTimeCalendarService,
    logger: Logger,
):
    test_member = make_test_member()
    test_member.user_content = "發出召集令"
    test_member.intent = UserIntent.NOTIFY_AGAIN.value
    test_member.is_attending = None

    test_command = make_use_case_command()
    test_command.member = test_member

    played_date = datetime_calendar_service.get_played_date()
    today_name = datetime_calendar_service.get_today_name()
    reminder_message = message_generator.get_reminder_message(
        played_date=played_date,
        today_name=today_name,
    )

    pending_members = PENDING_MEMBERS
    for member in pending_members:
        await member_profile_repo.save(member=member)

    use_case = NotifyAgainUseCase(
        member_profile_repo=member_profile_repo,
        message_service=line_message_service_mock,
        message_generator=message_generator,
        calendar=datetime_calendar_service,
        logger=logger,
    )

    result = await use_case.execute(cmd=test_command)

    expected_calls = [call(user_id=m.user_id, message=reminder_message) for m in pending_members]
    line_message_service_mock.push_message.assert_has_calls(expected_calls, any_order=True)

    assert line_message_service_mock.push_message.call_count == len(pending_members)
    assert result == "Handle notify process successful"
