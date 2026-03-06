from collections.abc import Generator
from contextlib import contextmanager
from logging import Logger

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from infrastructure.setting import config

_engine = create_engine(config.SQLALCHEMY.DATABASE_PATH)
_SessionFactory = sessionmaker(bind=_engine)


class SQLAlchemyContext:
    def __init__(self, logger: Logger):
        self.logger = logger

    @contextmanager
    def begin(self) -> Generator[Session, None, None]:
        session: Session = _SessionFactory()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    def init_db(self):
        from infrastructure.sqlalchemy.models import Base

        try:
            Base.metadata.create_all(bind=_engine)
            self.logger.info(f"資料庫初始化完成: {config.SQLALCHEMY.DATABASE_PATH}")
        except Exception as e:
            raise ConnectionError("Database init failed") from e
