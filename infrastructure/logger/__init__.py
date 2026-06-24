import logging
from logging import Handler, Logger

from opentelemetry._logs import LoggerProvider
from opentelemetry.sdk._logs import LoggingHandler as OTELLoggingHandler

from infrastructure.opentelemetry import otel_trace_record_factory

from .formatter import formatter, formatter_with_level
from .handler import get_otel_handler, get_stream_handler


def setup_logger(logger_provider: LoggerProvider | None) -> Logger:
    logging.getLogger("apscheduler").setLevel(logging.WARNING)
    logging.getLogger("uvicorn.error").setLevel(logging.WARNING)
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)

    logging.setLogRecordFactory(otel_trace_record_factory)
    logger_ = logging.getLogger()

    handlers: list[Handler] = [get_otel_handler(logger_provider=logger_provider), get_stream_handler()]

    logger_.setLevel(logging.INFO)

    for handler_ in handlers:
        if isinstance(handler_, OTELLoggingHandler):
            handler_.setFormatter(formatter)
        else:
            handler_.setFormatter(formatter_with_level)

        handler_.setLevel(logging.NOTSET)
        logger_.addHandler(handler_)
        logger_.propagate = False

    return logger_
