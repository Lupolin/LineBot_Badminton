from dataclasses import dataclass


@dataclass
class Absentee:
    user_name: str
    absent_count: int
