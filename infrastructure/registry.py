import logging
from dataclasses import dataclass
from functools import cached_property
from logging import Logger

from fastapi import FastAPI
from opentelemetry import trace
from opentelemetry._logs import LoggerProvider, set_logger_provider
from opentelemetry.trace import TracerProvider

from infrastructure.sqlalchemy.repositories import (
    AttendanceRecordRepositoryImpl,
    MemberRepositoryImpl,
)

from .http import HttpContext
from .line import (
    DateTimeCalendarServiceImpl,
    LineMessagingApiClientImpl,
    LineProfileApiClientImpl,
    LineWebhookEventParserImpl,
)
from .logger import setup_logger
from .opentelemetry import (
    create_logger_provider,
    create_resource,
    create_tracer_provider,
    setup_opentelemetry_instrumentor,
)
from .scheduler import SchedulerService
from .setting import Config
from .sqlalchemy import SQLAlchemyContext


@dataclass
class Registry:
    config: Config

    @cached_property
    def logger(self) -> Logger:
        return logging.getLogger(__name__)

    @cached_property
    def http(self) -> HttpContext:
        return HttpContext(logger=self.logger)

    @cached_property
    def session_factory(self) -> SQLAlchemyContext:
        return SQLAlchemyContext.from_config(database_url=self.config.SQLALCHEMY.DATABASE_URL)

    @cached_property
    def scheduler_service(self) -> SchedulerService:
        return SchedulerService(
            timezone=self.config.TIMEZONE,
            logger=self.logger,
        )

    @cached_property
    def datetime_calendar_service(self) -> DateTimeCalendarServiceImpl:
        return DateTimeCalendarServiceImpl(logger=self.logger)

    @cached_property
    def line_api_service(self) -> LineProfileApiClientImpl:
        return LineProfileApiClientImpl(
            http=self.http,
            logger=self.logger,
        )

    @cached_property
    def line_message_handler(self) -> LineWebhookEventParserImpl:
        return LineWebhookEventParserImpl(logger=self.logger)

    @cached_property
    def line_message_service(self) -> LineMessagingApiClientImpl:
        return LineMessagingApiClientImpl(
            logger=self.logger,
            access_token=self.config.LINE_BOT.CHANNEL_ACCESS_TOKEN,
        )

    @cached_property
    def member_profile_repo(self) -> MemberRepositoryImpl:
        return MemberRepositoryImpl(
            session_factory=self.session_factory,
            logger=self.logger,
        )

    @cached_property
    def attendance_record_repo(self) -> AttendanceRecordRepositoryImpl:
        return AttendanceRecordRepositoryImpl(
            session_factory=self.session_factory,
            logger=self.logger,
        )

    @cached_property
    def get_opentelemetry_provider(self) -> tuple[LoggerProvider | None, TracerProvider | None]:
        if not self.config.OPENTELEMETRY.ENABLE:
            return None, None

        resource = create_resource(service_name=self.config.SERVICE_NAME)

        logger_provider = create_logger_provider(
            otel_endpoint=self.config.OPENTELEMETRY.ENDPOINT,
            otel_enable=self.config.OPENTELEMETRY.ENABLE,
            resource=resource,
        )

        tracer_provider = create_tracer_provider(
            otel_endpoint=self.config.OPENTELEMETRY.ENDPOINT,
            otel_enable=self.config.OPENTELEMETRY.ENABLE,
            resource=resource,
        )

        return logger_provider, tracer_provider

    @cached_property
    def setup_logger(self) -> Logger:
        return setup_logger(logger_provider=self.get_opentelemetry_provider[0])

    def setup_opentelemetry(self) -> None:
        logger_provider, tracer_provider = self.get_opentelemetry_provider

        if logger_provider is not None:
            set_logger_provider(logger_provider)

        if tracer_provider is not None:
            trace.set_tracer_provider(tracer_provider)

    def setup_opentelemetry_instrumentor(self, app: FastAPI, excluded_urls: list[str]) -> None:
        if self.config.OPENTELEMETRY.ENABLE:
            setup_opentelemetry_instrumentor(
                app=app,
                excluded_urls=excluded_urls,
            )
