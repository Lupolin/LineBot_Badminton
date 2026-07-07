from unittest.mock import ANY

import pytest

from app.interaction import IntentDispatcher
from app.interaction.dispatcher import IntentDispatcherCommand


@pytest.fixture
def dispatcher(
    registry_mock,
    member_profile_repo_mock,
    line_message_service_mock,
    logger,
):
    return IntentDispatcher(
        registry=registry_mock,
        member_profile_repo=member_profile_repo_mock,
        message_service=line_message_service_mock,
        logger=logger,
    )


@pytest.mark.asyncio
async def test_dispatch_success(
    dispatcher,
    registry_mock,
    use_case_mock,
    member_profile_repo_mock,
):
    test_cmd = IntentDispatcherCommand(
        user_id="U001",
        user_content="統計",
        reply_token="fake_token",
    )
    result = await dispatcher.execute(test_cmd)

    member_profile_repo_mock.find_by_id.assert_awaited_once_with(test_cmd.user_id)
    registry_mock.get_use_case_by_intent.assert_called_once()

    use_case_mock.execute.assert_awaited_once_with(ANY)

    assert result == "Mock UseCase executed"
