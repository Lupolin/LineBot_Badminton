from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Index,
    Integer,
    String,
    func,
)

from .base import Base


class MemberProfile(Base):
    __tablename__ = "MemberProfile"
    __table_args__ = {"schema": "LineBot"}


    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String(40), index=True, nullable=False, unique=True)
    user_name = Column(String(32), nullable=False)
    user_content = Column(String(20), nullable=False)
    role = Column(String(20), nullable=False)
    is_attending = Column(Boolean, default=False)
    intent = Column(String(32), nullable=True, default=None)
    played_date = Column(String(5), nullable=True)
    last_replied_at = Column(DateTime, nullable=True, default=None)
    timestamp = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())
