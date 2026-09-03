from unittest.mock import ANY

import pytest

from app.interaction.use_cases import RegisterMemberUseCase
from domain.entity import (
    UserIntent,
)
from tests.mock_data import make_use_case_command


@pytest.fixture
def register_member_use_case(
    member_profile_repo_mock,
    line_message_service_mock,
    line_api_service_mock,
    logger,
):
    return RegisterMemberUseCase(
        member_profile_repo=member_profile_repo_mock,
        message_service=line_message_service_mock,
        api_service=line_api_service_mock,
        logger=logger,
    )


@pytest.mark.asyncio
async def test_register_member_success(
    register_member_use_case,
    member_profile_repo_mock,
    line_message_service_mock,
    line_api_service_mock,
    logger,
):
    test_command = make_use_case_command()
    test_command.user_content = "註冊"
    test_command.intent = UserIntent.REGISTER

    result = await register_member_use_case.execute(cmd=test_command)

    line_api_service_mock.get_user_name.assert_called_once_with(user_id=test_command.user_id)
    user_name = line_api_service_mock.get_user_name.return_value
    assert user_name == "Lucas"

    member_profile_repo_mock.save.assert_awaited_once_with(member=ANY)

    assert result == "註冊好了！\n我再也不會忘記你了！"
