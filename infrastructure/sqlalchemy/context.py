from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from dataclasses import dataclass
from logging import Logger

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from infrastructure.setting import config

_engine = create_async_engine(
    config.SQLALCHEMY.DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=1800,
    pool_size=5,
    max_overflow=10,
)
_SessionFactory = async_sessionmaker(bind=_engine)


@dataclass
class SQLAlchemyContext:
    logger: Logger

    @asynccontextmanager
    async def begin(self) -> AsyncGenerator[AsyncSession, None]:
        async with _SessionFactory() as session:
            async with session.begin():
                yield session
