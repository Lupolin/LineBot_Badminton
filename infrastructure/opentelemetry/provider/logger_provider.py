from opentelemetry.exporter.otlp.proto.http._log_exporter import OTLPLogExporter
from opentelemetry.sdk._logs import LoggerProvider
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
from opentelemetry.sdk.resources import Resource


def create_logger_provider(otel_endpoint: str | None, otel_enable: bool, resource: Resource) -> LoggerProvider | None:
    if not otel_enable:
        return None

    log_exporter: OTLPLogExporter = OTLPLogExporter(endpoint=f"{otel_endpoint}/v1/logs")
    logger_provider: LoggerProvider = LoggerProvider(resource=resource)
    logger_provider.add_log_record_processor(BatchLogRecordProcessor(log_exporter))

    return logger_provider
