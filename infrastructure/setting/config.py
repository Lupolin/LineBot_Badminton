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
class FlaskConfig:
    HOST: str = "0.0.0.0"
    PORT: int = 8080
    DEBUG: bool = False

    @classmethod
    def from_env(cls):
        return cls(
            HOST=os.getenv("HOST", "0.0.0.0"),
            PORT=int(os.getenv("PORT", "8080")),
            DEBUG=os.getenv("DEBUG", "false").lower() == "true",
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
    ENDPOINT: str = "http://localhost:4318/v1/traces"

    @classmethod
    def from_env(cls):
        return cls(
            ENDPOINT=os.getenv(
                "OPENTELEMETRY_ENDPOINT",
                "http://localhost:4318/v1/traces",
            ),
        )


@dataclass(frozen=True)
class Config:
    FLASK: FlaskConfig = field(default_factory=FlaskConfig.from_env)
    LINE_BOT: LineBotConfig = field(default_factory=LineBotConfig.from_env)
    SQLALCHEMY: SQLAlchemyConfig = field(default_factory=SQLAlchemyConfig.from_env)
    OPENTELEMETRY: OpenTelemetryConfig = field(default_factory=OpenTelemetryConfig.from_env)
    TIMEZONE: str = "Asia/Taipei"
    BADMINTON_TIME: str = "18-20"
    BADMINTON_LOCATION: str = "信義國小"
    SERVICE_NAME: str = "line-bot-backend"

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
