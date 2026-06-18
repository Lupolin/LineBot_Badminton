from dataclasses import dataclass


@dataclass
class Admin:
    user_id: str
    user_role: str
