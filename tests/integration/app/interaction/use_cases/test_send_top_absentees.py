from logging import Logger
from unittest.mock import Mock

import pytest

from app.interaction.use_cases import SendTopAbsenteeUseCase
from domain.entity import UserIntent
from domain.repository import AttendanceRecordRepository, MemberProfileRepository
from domain.service import MessageGenerator
from tests.mock_data import (
    ALL_ATTENDANCE,
    make_test_member,
    make_use_case_command,
)


@pytest.mark.asyncio
async def test_send_top_absentee_use_case(
    member_profile_repo: MemberProfileRepository,
    attendance_record_repo: AttendanceRecordRepository,
    line_message_service_mock: Mock,
    message_generator: MessageGenerator,
    logger: Logger,
):
    test_member = make_test_member()
    all_attendance = ALL_ATTENDANCE

    await member_profile_repo.save(member=test_member)
    await attendance_record_repo.save_all(records=all_attendance)

    test_member.user_content = "誰是請假王"
    test_member.intent = UserIntent.ABSENTEE.value
    test_member.is_attending = None

    test_command = make_use_case_command()
    test_command.user_content = test_member.user_content
    test_command.member = test_member

    use_case = SendTopAbsenteeUseCase(
        member_profile_repo=member_profile_repo,
        attendance_record_repo=attendance_record_repo,
        message_service=line_message_service_mock,
        message_generator=message_generator,
        logger=logger,
    )

    result = await use_case.execute(cmd=test_command)

    raw_list = await attendance_record_repo.find_top_absentees()
    top_absentee_list = raw_list if raw_list is not None else []

    message = message_generator.get_attendance_result_message(absentee=top_absentee_list)

    line_message_service_mock.reply_message.assert_called_once_with(
        reply_token=test_command.reply_token,
        message=message,
    )

    assert result == message
