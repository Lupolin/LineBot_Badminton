import os
from dataclasses import dataclass

from dotenv import load_dotenv


@dataclass(frozen=True)
class LineBotConfig:
    CHANNEL_SECRET: str
    CHANNEL_ACCESS_TOKEN: str
    PROFILE_ENDPOINT: str
    REPLY_ENDPOINT: str


@dataclass(frozen=True)
class SQLAlchemyConfig:
    DATABASE_URL: str


@dataclass(frozen=True)
class OpenTelemetryConfig:
    ENDPOINT: str | None
    ENABLE: bool


@dataclass(frozen=True)
class MessageConfig:
    TIME: str
    LOCATION: str


@dataclass(frozen=True)
class Config:
    LINE_BOT: LineBotConfig
    SQLALCHEMY: SQLAlchemyConfig
    OPENTELEMETRY: OpenTelemetryConfig
    MESSAGE: MessageConfig
    TIMEZONE: str
    SERVICE_NAME: str

    def validate(self):
        errors = []
        if not self.LINE_BOT.CHANNEL_SECRET:
            errors.append("LINE_CHANNEL_SECRET is missing")
        if not self.LINE_BOT.CHANNEL_ACCESS_TOKEN:
            errors.append("LINE_CHANNEL_ACCESS_TOKEN is missing")
        if not self.SQLALCHEMY.DATABASE_URL:
            errors.append("DATABASE_URL is missing")

        if errors:
            raise ValueError(f"Configuration validation failed: {', '.join(errors)}")

    @classmethod
    def from_env(cls):
        env = os.environ.get("ENV", "dev")
        file_name = f".env.{env}"

        if os.path.exists(file_name):
            load_dotenv(dotenv_path=file_name)

        config = cls(
            LINE_BOT=LineBotConfig(
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
            ),
            SQLALCHEMY=SQLAlchemyConfig(DATABASE_URL=os.getenv("DATABASE_URL", "")),
            OPENTELEMETRY=OpenTelemetryConfig(
                ENDPOINT=os.getenv("OPENTELEMETRY_ENDPOINT"),
                ENABLE=os.getenv("OPENTELEMETRY_ENABLE", "false").lower() == "true",
            ),
            MESSAGE=MessageConfig(
                TIME=os.getenv("BADMINTON_TIME", "18-20"),
                LOCATION=os.getenv("BADMINTON_LOCATION", "信義國小"),
            ),
            TIMEZONE="Asia/Taipei",
            SERVICE_NAME="LineBot_Badminton",
        )

        config.validate()

        return config
