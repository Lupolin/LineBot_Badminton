import pytest

from app.interaction.use_cases import QueryStatUseCase
from domain.entity import (
    UserIntent,
)
from tests.mock_data import make_test_member, make_use_case_command


@pytest.fixture
def query_stat_use_case(
    member_profile_repo_mock,
    line_message_service_mock,
    message_generator,
    datetime_calendar_service_mock,
    logger,
):
    return QueryStatUseCase(
        member_profile_repo=member_profile_repo_mock,
        message_service=line_message_service_mock,
        message_generator=message_generator,
        calendar=datetime_calendar_service_mock,
        logger=logger,
    )


@pytest.mark.asyncio
async def test_query_stat_success(
    query_stat_use_case,
    member_profile_repo_mock,
    line_message_service_mock,
    message_generator,
    datetime_calendar_service_mock,
    logger,
):
    test_member = make_test_member()
    test_member.user_content = "統計"
    test_command = make_use_case_command()
    test_command.user_content = test_member.user_content
    test_command.intent = UserIntent.QUERY_STAT
    test_command.member = test_member

    result = await query_stat_use_case.execute(cmd=test_command)

    datetime_calendar_service_mock.get_played_date.assert_called_once_with()
    member_profile_repo_mock.get_attending_members.assert_awaited_once_with()
    member_profile_repo_mock.get_not_attending_members.assert_awaited_once_with()
    member_profile_repo_mock.get_pending_members.assert_awaited_once_with()
    member_profile_repo_mock.save.assert_awaited_once_with(member=test_command.member)

    attending_members = member_profile_repo_mock.get_attending_members.return_value
    not_attending_members = member_profile_repo_mock.get_not_attending_members.return_value
    pending_members = member_profile_repo_mock.get_pending_members.return_value

    summary_message = message_generator.get_summary_message(
        played_date="07/03",
        attending_members=attending_members,
        not_attending_members=not_attending_members,
        pending_members=pending_members,
    )

    line_message_service_mock.reply_message.assert_called_once_with(
        reply_token=test_command.reply_token,
        message=summary_message,
    )

    assert result == summary_message
