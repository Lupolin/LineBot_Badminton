from dataclasses import dataclass


@dataclass
class Attendance:
    user_id: str
    user_name: str
    played_date: str
    is_attending: bool | None = None
