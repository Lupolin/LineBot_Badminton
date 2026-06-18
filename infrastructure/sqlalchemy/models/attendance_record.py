from datetime import datetime

from sqlalchemy import (
    Boolean,
    DateTime,
    Integer,
    String,
    func,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from .base import Base


class AttendanceRecord(Base):
    __tablename__ = "AttendanceRecord"
    __table_args__ = {"schema": "LineBot"}

    id: Mapped[int] = mapped_column("Id", Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[str] = mapped_column("UserId", String(40), index=True, nullable=False)
    user_name: Mapped[str] = mapped_column("UserName", String(40), nullable=False)
    is_attending: Mapped[bool | None] = mapped_column("isAttending", Boolean, nullable=False, default=False)
    played_date: Mapped[str] = mapped_column("PlayedDate", String, nullable=False)
    timestamp: Mapped[datetime] = mapped_column(
        "TimeStamp", DateTime, nullable=False, server_default=func.now(), onupdate=func.now()
    )
