from collections.abc import AsyncGenerator
from logging import Logger, getLogger
from typing import Any
from unittest.mock import AsyncMock, Mock

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.registry import Registry as App_Registry
from domain.entity import BadmintonMessages
from domain.service import MessageGenerator
from infrastructure.line import (
    DateTimeCalendarServiceImpl,
    LineApiServiceImpl,
    LineMessageHandlerImpl,
    LineMessageServiceImpl,
)
from infrastructure.registry import Registry as Infra_Registry
from infrastructure.setting import Config
from infrastructure.sqlalchemy.context import SQLAlchemyContext
from infrastructure.sqlalchemy.models import Base
from infrastructure.sqlalchemy.repositories import AttendanceRecordRepositoryImpl, MemberRepositoryImpl
from tests.mock_data import MESSAGE_EVENT


@pytest.fixture(scope="function")
def logger() -> Logger:
    return getLogger("test_logger")


@pytest.fixture()
def http() -> AsyncMock:
    return AsyncMock()


@pytest.fixture(scope="session")
def config() -> Config:
    return Config.from_env()


@pytest.fixture(scope="function")
def infra_registry(config: Config) -> Infra_Registry:
    return Infra_Registry(config=config)


@pytest.fixture(scope="function")
def app_registry() -> App_Registry:
    return App_Registry()


@pytest.fixture(scope="function")
async def sqlalchemy_context(config: Config) -> AsyncGenerator[Any, Any]:
    context = SQLAlchemyContext.from_config(config.SQLALCHEMY.DATABASE_URL)
    yield context


@pytest.fixture(scope="function")
async def db_session(sqlalchemy_context: SQLAlchemyContext) -> AsyncGenerator[AsyncSession, None]:
    connection = await sqlalchemy_context.engine.connect()
    transaction = await connection.begin()

    session = AsyncSession(bind=connection, join_transaction_mode="create_savepoint")

    yield session

    await session.close()
    await transaction.rollback()
    await connection.close()


@pytest.fixture(autouse=True)
async def clean_db(sqlalchemy_context: SQLAlchemyContext) -> None:
    # 這段代碼會在每個測試開始前執行，確保資料庫清空
    async with sqlalchemy_context.engine.begin() as conn:
        await conn.run_sync(Base.metadata.reflect)
        for table in reversed(Base.metadata.sorted_tables):
            await conn.execute(table.delete())


@pytest.fixture(scope="function")
def member_profile_repo(infra_registry: Infra_Registry) -> MemberRepositoryImpl:
    return infra_registry.member_profile_repo


@pytest.fixture(scope="function")
def attendance_record_repo(infra_registry: Infra_Registry) -> AttendanceRecordRepositoryImpl:
    return infra_registry.attendance_record_repo


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


@pytest.fixture(scope="function")
def message_generator() -> MessageGenerator:
    return MessageGenerator(messages=BadmintonMessages())


@pytest.fixture(scope="function")
def datetime_calendar_service(infra_registry: Infra_Registry) -> DateTimeCalendarServiceImpl:
    return infra_registry.datetime_calendar_service
