import logging

from opentelemetry._logs import LoggerProvider
from opentelemetry.sdk._logs import LoggingHandler


def get_otel_handler(logger_provider: LoggerProvider | None, handler_name: str | None = None) -> LoggingHandler:
    otel_handler = LoggingHandler(level=logging.NOTSET, logger_provider=logger_provider)
    otel_handler.set_name(handler_name if handler_name else "otel-handler")
    return otel_handler
