import os
from dataclasses import dataclass, field

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class LineBotConfig:
    CHANNEL_SECRET: str
    CHANNEL_ACCESS_TOKEN: str
    PROFILE_ENDPOINT: str
    REPLY_ENDPOINT: str

    @classmethod
    def from_env(cls):
        return cls(
            CHANNEL_SECRET=os.getenv("LINE_CHANNEL_SECRET", ""),
            CHANNEL_ACCESS_TOKEN=os.getenv("LINE_CHANNEL_ACCESS_TOKEN", ""),
            PROFILE_ENDPOINT=os.getenv(
                "LINE_PROFILE_ENDPOINT",
                "https://api.line.me/v2/bot/profile",
            ),
            REPLY_ENDPOINT=os.getenv(
                "REPLY_ENDPOINT",
                "https://api.line.me/v2/bot/message/reply",
            ),
        )

@dataclass(frozen=True)
class SQLAlchemyConfig:
    DATABASE_PATH: str

    @classmethod
    def from_env(cls):
        return cls(
            DATABASE_PATH=os.getenv("DATABASE_PATH", ""),
        )


@dataclass(frozen=True)
class OpenTelemetryConfig:
    ENDPOINT: str | None
    ENABLE: bool

    @classmethod
    def from_env(cls):
        return cls(
            ENDPOINT=os.getenv("OPENTELEMETRY_ENDPOINT"),
            ENABLE=os.getenv("OPENTELEMETRY_ENABLE", "false").lower() == "true",
        )

@dataclass(frozen=True)
class MessageConfig:
    TIME: str
    LOCATION: str

    @classmethod
    def from_env(cls):
        return cls(
            TIME=os.getenv("BADMINTON_TIME"),
            LOCATION=os.getenv("BADMINTON_LOCATION"),
        )

@dataclass(frozen=True)
class Config:
    LINE_BOT: LineBotConfig = field(default_factory=LineBotConfig.from_env)
    SQLALCHEMY: SQLAlchemyConfig = field(default_factory=SQLAlchemyConfig.from_env)
    OPENTELEMETRY: OpenTelemetryConfig = field(default_factory=OpenTelemetryConfig.from_env)
    MESSAGE: MessageConfig = field(default_factory=MessageConfig.from_env)
    TIMEZONE: str = "Asia/Taipei"
    SERVICE_NAME: str = "LineBot_Badminton"

    def __post_init__(self):
        self.validate()

    def validate(self):
        errors = []
        if not self.LINE_BOT.CHANNEL_SECRET:
            errors.append("LINE_CHANNEL_SECRET is missing")
        if not self.LINE_BOT.CHANNEL_ACCESS_TOKEN:
            errors.append("LINE_CHANNEL_ACCESS_TOKEN is missing")
        if not self.SQLALCHEMY.DATABASE_PATH:
            errors.append("DATABASE_PATH is missing")

        if errors:
            raise ValueError(f"Configuration validation failed: {', '.join(errors)}")


# 單一出口點
config = Config()
