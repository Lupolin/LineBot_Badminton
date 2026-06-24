from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from dataclasses import dataclass

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)


@dataclass
class SQLAlchemyContext:
    engine: AsyncEngine
    _session_factory: async_sessionmaker[AsyncSession]

    @classmethod
    def from_config(cls, database_url: str):
        engine = create_async_engine(
            database_url,
            pool_pre_ping=True,
            pool_recycle=1800,
            pool_size=5,
            max_overflow=10,
        )
        session_factory = async_sessionmaker(bind=engine)
        return cls(engine=engine, _session_factory=session_factory)

    @asynccontextmanager
    async def begin(self) -> AsyncGenerator[AsyncSession, None]:
        async with self._session_factory() as session:
            async with session.begin():
                yield session
