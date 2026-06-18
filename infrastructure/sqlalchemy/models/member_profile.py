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


class MemberProfile(Base):
    __tablename__ = "MemberProfile"
    __table_args__ = {"schema": "LineBot"}

    id: Mapped[int] = mapped_column("Id", Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[str] = mapped_column("UserId", String(40), index=True, nullable=False, unique=True)
    user_name: Mapped[str] = mapped_column("UserName", String(40), nullable=False)
    user_content: Mapped[str] = mapped_column("UserContent", String(20), nullable=False)
    role: Mapped[str] = mapped_column("Role", String(20), nullable=False)
    is_attending: Mapped[bool | None] = mapped_column("isAttending", Boolean, nullable=True, default=False)
    intent: Mapped[str | None] = mapped_column("Intent", String(32), nullable=True, default=None)
    played_date: Mapped[str | None] = mapped_column("PlayedDate", String(5), nullable=True)
    status: Mapped[str | None] = mapped_column("Status", String(10), nullable=True)
    last_replied_at: Mapped[datetime | None] = mapped_column("LastRepliedAt", DateTime, nullable=True, default=None)
    timestamp: Mapped[datetime] = mapped_column(
        "TimeStamp", DateTime, nullable=False, server_default=func.now(), onupdate=func.now()
    )
