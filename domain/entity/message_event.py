from dataclasses import dataclass


@dataclass
class MessageEvent:
    user_id: str
    user_content: str
    reply_token: str
