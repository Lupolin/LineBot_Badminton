from logging import Logger
from unittest.mock import Mock

import pytest

from app.interaction import IntentDispatcher
from app.registry import Registry as App_Registry
from domain.repository import MemberProfileRepository
from tests.mock_data import make_intent_dispatcher_command, make_test_member


@pytest.mark.asyncio
async def test_dispatcher(
    app_registry: App_Registry,
    member_profile_repo: MemberProfileRepository,
    line_message_service_mock: Mock,
    logger: Logger,
):
    test_member = make_test_member()
    test_command = make_intent_dispatcher_command()
    test_command.user_id = test_member.user_id
    test_command.user_content = test_member.user_content

    await member_profile_repo.save(member=test_member)

    use_case = IntentDispatcher(
        registry=app_registry,
        member_profile_repo=member_profile_repo,
        message_service=line_message_service_mock,
        logger=logger,
    )

    result = await use_case.execute(cmd=test_command)

    assert "Handle attendance process successful" in result
