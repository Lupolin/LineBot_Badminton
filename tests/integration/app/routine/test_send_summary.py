from logging import Logger
from unittest.mock import Mock

import pytest

from app.routine import SendSummaryUseCase
from domain.gateway import DateTimeCalendarService
from domain.repository import MemberProfileRepository
from domain.service import MessageGenerator
from tests.mock_data import (
    ATTENDING_MEMBERS,
    MEMBER_PROFILE_DATA,
    NOT_ATTENDING_MEMBERS,
    PENDING_MEMBERS,
    make_test_admin,
)


@pytest.mark.asyncio
async def test_send_summary_use_case(
    member_profile_repo: MemberProfileRepository,
    line_message_service_mock: Mock,
    message_generator: MessageGenerator,
    datetime_calendar_service: DateTimeCalendarService,
    logger: Logger,
):
    pending_members = PENDING_MEMBERS
    attending_members = ATTENDING_MEMBERS
    not_attending_members = NOT_ATTENDING_MEMBERS
    member_profile_data = MEMBER_PROFILE_DATA

    for member in member_profile_data:
        await member_profile_repo.save(member=member)

    test_admin = make_test_admin()
    await member_profile_repo.save(member=test_admin)

    use_case = SendSummaryUseCase(
        member_profile_repo=member_profile_repo,
        message_service=line_message_service_mock,
        message_generator=message_generator,
        calendar=datetime_calendar_service,
        logger=logger,
    )

    await use_case.execute()

    played_date = datetime_calendar_service.get_played_date()
    get_attending_members = await member_profile_repo.get_attending_members()
    get_not_attending_members = await member_profile_repo.get_not_attending_members()
    get_pending_members = await member_profile_repo.get_pending_members()

    summary_message = message_generator.get_summary_message(
        played_date=played_date,
        attending_members=attending_members,
        not_attending_members=not_attending_members,
        pending_members=pending_members,
    )

    assert len(get_attending_members) == len(attending_members)
    assert len(get_pending_members) == len(attending_members)
    assert len(get_not_attending_members) == len(not_attending_members)

    line_message_service_mock.push_message.assert_called_once_with(
        user_id=test_admin.user_id,
        message=summary_message,
    )
