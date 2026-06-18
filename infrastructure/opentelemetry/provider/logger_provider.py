from opentelemetry._logs import set_logger_provider
from opentelemetry.exporter.otlp.proto.http._log_exporter import OTLPLogExporter
from opentelemetry.sdk._logs import LoggerProvider
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor

from infrastructure.opentelemetry.resource import resource
from infrastructure.setting import config

log_exporter: OTLPLogExporter = OTLPLogExporter(endpoint=f"{config.OPENTELEMETRY.ENDPOINT}/v1/logs")

logger_provider: LoggerProvider = LoggerProvider(resource=resource)

logger_provider.add_log_record_processor(BatchLogRecordProcessor(log_exporter))


def setup_logger_provider():
    set_logger_provider(logger_provider)
