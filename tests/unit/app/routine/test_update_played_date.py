import pytest

from app.routine import UpdatePlayedDateUseCase


@pytest.fixture
def update_played_date_use_case(
    member_profile_repo_mock,
    datetime_calendar_service_mock,
    logger,
):
    return UpdatePlayedDateUseCase(
        member_profile_repo=member_profile_repo_mock,
        calendar=datetime_calendar_service_mock,
        logger=logger,
    )


@pytest.mark.asyncio
async def test_update_played_date_success(
    update_played_date_use_case,
    member_profile_repo_mock,
    datetime_calendar_service_mock,
    logger,
):
    await update_played_date_use_case.execute()

    datetime_calendar_service_mock.get_played_date.assert_called_once_with()
    played_date = datetime_calendar_service_mock.get_played_date.return_value

    member_profile_repo_mock.update_played_date.assert_awaited_once_with(played_date=played_date)
