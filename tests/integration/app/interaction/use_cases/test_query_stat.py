from logging import Logger
from unittest.mock import Mock

import pytest

from app.interaction.use_cases import QueryStatUseCase
from domain.entity import UserIntent
from domain.gateway import DateTimeCalendarService
from domain.repository import MemberProfileRepository
from domain.service import MessageGenerator
from tests.mock_data import (
    ATTENDING_MEMBERS,
    MEMBER_PROFILE_DATA,
    NOT_ATTENDING_MEMBERS,
    PENDING_MEMBERS,
    make_test_member,
    make_use_case_command,
)


@pytest.mark.asyncio
async def test_query_stat_use_case(
    member_profile_repo: MemberProfileRepository,
    line_message_service_mock: Mock,
    message_generator: MessageGenerator,
    datetime_calendar_service: DateTimeCalendarService,
    logger: Logger,
):
    played_date = datetime_calendar_service.get_played_date()
    attending_members = ATTENDING_MEMBERS
    not_attending_members = NOT_ATTENDING_MEMBERS
    pending_members = PENDING_MEMBERS
    member_profile_data = MEMBER_PROFILE_DATA

    for member in member_profile_data:
        await member_profile_repo.save(member=member)

    test_member = make_test_member()
    test_member.user_content = "統計"
    test_member.intent = UserIntent.QUERY_STAT.value

    test_command = make_use_case_command()
    test_command.user_content = test_member.user_content
    test_command.member = test_member

    use_case = QueryStatUseCase(
        member_profile_repo=member_profile_repo,
        message_service=line_message_service_mock,
        message_generator=message_generator,
        calendar=datetime_calendar_service,
        logger=logger,
    )

    result = await use_case.execute(cmd=test_command)

    summary_message = message_generator.get_summary_message(
        played_date=played_date,
        attending_members=attending_members,
        not_attending_members=not_attending_members,
        pending_members=pending_members,
    )

    line_message_service_mock.reply_message.assert_called_once_with(
        reply_token=test_command.reply_token,
        message=summary_message,
    )

    assert result == summary_message
