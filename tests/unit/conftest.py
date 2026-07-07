from logging import (
    Logger,
    getLogger,
)
from typing import Any
from unittest.mock import (
    AsyncMock,
    Mock,
)

import pytest

from domain.entity import BadmintonMessages
from domain.service import MessageGenerator
from infrastructure.line import (
    DateTimeCalendarServiceImpl,
    LineApiServiceImpl,
    LineMessageHandlerImpl,
    LineMessageServiceImpl,
)
from infrastructure.sqlalchemy.repositories import (
    AttendanceRecordRepositoryImpl,
    MemberRepositoryImpl,
)
from tests.unit.mock_data import (
    ADMIN_MEMBERS_LIST,
    ALL_ATTENDANCE_LIST,
    ATTENDING_MEMBERS_LIST,
    FIND_BY_ID,
    MESSAGE_EVENT,
    NOT_ATTENDING_MEMBERS_LIST,
    PENDING_MEMBERS_LIST,
    TOP_ABSENTEES_LIST,
)


@pytest.fixture(scope="session")
def logger() -> Logger:
    return getLogger("test_logger")


@pytest.fixture()
def http() -> AsyncMock:
    return AsyncMock()


@pytest.fixture()
def session_factory() -> AsyncMock:
    return AsyncMock()


@pytest.fixture
def use_case_mock():
    use_case = Mock()
    use_case.execute = AsyncMock(return_value="Mock UseCase executed")
    return use_case


@pytest.fixture()
def registry_mock(use_case_mock: Mock) -> Mock:
    registry = Mock()
    registry.get_use_case_by_intent.return_value = use_case_mock
    return registry


@pytest.fixture
def message_generator() -> MessageGenerator:
    return MessageGenerator(messages=BadmintonMessages())


@pytest.fixture
def line_api_service_mock(logger: Logger, http: AsyncMock) -> LineApiServiceImpl:
    service = LineApiServiceImpl(
        logger=logger,
        http=http,
    )

    service.get_user_name = AsyncMock(return_value="Lucas")
    service.reply_message = AsyncMock()

    return service


@pytest.fixture
def line_message_handler_mock(logger: Logger) -> LineMessageHandlerImpl:
    service = LineMessageHandlerImpl(logger=logger)

    service.parse_webhook_body = AsyncMock(return_value=[MESSAGE_EVENT])

    return service


@pytest.fixture
def line_message_service_mock(logger: Logger) -> Mock:
    service = Mock(spec=LineMessageServiceImpl)
    service.logger = logger

    service.message_api = AsyncMock()
    service.push_message = AsyncMock()
    service.reply_message = AsyncMock()
    service.close = AsyncMock()

    return service


@pytest.fixture
def datetime_calendar_service_mock(logger: Logger) -> DateTimeCalendarServiceImpl:
    service = DateTimeCalendarServiceImpl(logger=logger)

    service.get_played_date = Mock(return_value="07/03")
    service.get_today_name = Mock(return_value="tuesday")

    return service


@pytest.fixture
def attendance_record_repo_mock(logger: Logger, session_factory: AsyncMock) -> Any:
    repo = AttendanceRecordRepositoryImpl(
        session_factory=session_factory,
        logger=logger,
    )

    repo.save_all = AsyncMock()
    repo.get_all_data = AsyncMock(return_value=ALL_ATTENDANCE_LIST)
    repo.find_all_data = AsyncMock(return_value=ALL_ATTENDANCE_LIST)
    repo.find_top_absentees = AsyncMock(return_value=TOP_ABSENTEES_LIST)

    return repo


@pytest.fixture
def member_profile_repo_mock(logger: Logger, session_factory: AsyncMock) -> Any:
    repo = MemberRepositoryImpl(
        session_factory=session_factory,
        logger=logger,
    )

    repo.get_pending_members = AsyncMock(return_value=PENDING_MEMBERS_LIST)
    repo.get_attending_members = AsyncMock(return_value=ATTENDING_MEMBERS_LIST)
    repo.get_not_attending_members = AsyncMock(return_value=NOT_ATTENDING_MEMBERS_LIST)
    repo.get_admin_members = AsyncMock(return_value=ADMIN_MEMBERS_LIST)
    repo.update_played_date = AsyncMock()
    repo.reset_all_attendance = AsyncMock()
    repo.save = AsyncMock()
    repo.find_by_id = AsyncMock(return_value=FIND_BY_ID)

    return repo
