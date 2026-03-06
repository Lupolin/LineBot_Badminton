from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

from infrastructure.opentelemetry.resource import resource
from infrastructure.setting import config

otlp_exporter: OTLPSpanExporter = OTLPSpanExporter(endpoint=f"{config.OPENTELEMETRY.ENDPOINT}/v1/traces")

tracer_provider: TracerProvider = TracerProvider(resource=resource)

tracer_provider.add_span_processor(BatchSpanProcessor(otlp_exporter))


def setup_tracer_provider():
    trace.set_tracer_provider(tracer_provider)
