from dataclasses import dataclass


@dataclass
class LineMessageEvent:
    user_id: str
    user_content: str
    reply_token: str
