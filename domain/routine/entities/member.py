from dataclasses import dataclass
from datetime import datetime


@dataclass
class Member:
    user_id: str
    user_name: str
    played_date: str
    is_attending: bool | None = None
    last_replied_at: datetime | None = None
