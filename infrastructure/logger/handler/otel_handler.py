import logging

from opentelemetry.sdk._logs import LoggingHandler

from infrastructure.opentelemetry.provider.logger_provider import logger_provider


def get_otel_handler(handler_name: str | None = None) -> LoggingHandler:
    otel_handler = LoggingHandler(level=logging.NOTSET, logger_provider=logger_provider)
    otel_handler.set_name(handler_name if handler_name else "otel-handler")
    return otel_handler
