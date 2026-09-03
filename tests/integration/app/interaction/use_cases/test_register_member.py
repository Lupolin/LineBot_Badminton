from logging import Logger
from unittest.mock import AsyncMock, Mock

import pytest

from app.interaction.use_cases import RegisterMemberUseCase
from domain.entity import UserIntent
from domain.repository import MemberProfileRepository
from tests.mock_data import make_test_member, make_use_case_command


@pytest.mark.asyncio
async def test_register_member_use_case_first_register(
    member_profile_repo: MemberProfileRepository,
    line_message_service_mock: Mock,
    line_api_service_mock: AsyncMock,
    logger: Logger,
):
    test_member = make_test_member()
    test_member.user_content = "註冊"
    test_member.intent = UserIntent.REGISTER.value
    test_member.is_attending = None

    test_command = make_use_case_command()
    test_command.user_content = test_member.user_content
    test_command.member = test_member

    use_case = RegisterMemberUseCase(
        member_profile_repo=member_profile_repo,
        message_service=line_message_service_mock,
        api_service=line_api_service_mock,
        logger=logger,
    )

    result = await use_case.execute(cmd=test_command)

    get_member = await member_profile_repo.find_by_id(user_id=test_command.user_id)

    assert get_member is not None
    assert get_member.status == "ACTIVE"
    assert get_member.role == "Member"
    assert result == "註冊好了！\n我再也不會忘記你了！"


@pytest.mark.asyncio
async def test_register_member_use_case_change_role_to_admin(
    member_profile_repo: MemberProfileRepository,
    line_message_service_mock: Mock,
    line_api_service_mock: AsyncMock,
    logger: Logger,
):
    existing_member = make_test_member()

    await member_profile_repo.save(member=existing_member)

    test_member = make_test_member()
    test_member.user_content = "Admin"
    test_member.intent = UserIntent.REGISTER.value

    test_command = make_use_case_command()
    test_command.user_content = test_member.user_content
    test_command.member = test_member

    use_case = RegisterMemberUseCase(
        member_profile_repo=member_profile_repo,
        message_service=line_message_service_mock,
        api_service=line_api_service_mock,
        logger=logger,
    )

    result = await use_case.execute(cmd=test_command)

    get_member = await member_profile_repo.find_by_id(user_id=test_command.user_id)

    assert get_member is not None
    assert get_member.role == "Admin"
    assert result == "偷偷跟你說喔！你是我的管理員了❤️"
