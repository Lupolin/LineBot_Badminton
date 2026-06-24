from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor


def create_tracer_provider(otel_endpoint: str | None, otel_enable: bool, resource: Resource) -> TracerProvider | None:
    if not otel_enable:
        return None

    otel_exporter: OTLPSpanExporter = OTLPSpanExporter(endpoint=f"{otel_endpoint}/v1/traces")
    tracer_provider: TracerProvider = TracerProvider(resource=resource)
    tracer_provider.add_span_processor(BatchSpanProcessor(otel_exporter))

    return tracer_provider
