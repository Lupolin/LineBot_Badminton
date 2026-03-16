from dataclasses import dataclass


@dataclass
class Attendance:
    user_id: str
    user_name: str
    is_attending: bool
    played_date: str
