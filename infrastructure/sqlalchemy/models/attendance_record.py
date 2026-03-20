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


class AttendanceRecord(Base):
    __tablename__ = "AttendanceRecord"
    __table_args__ = {"schema": "LineBot"}

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String(40), index=True, nullable=False)
    user_name = Column(String(32), nullable=False)
    is_attending = Column(Boolean, default=False)
    played_date = Column(String, nullable=False)
    timestamp = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())
