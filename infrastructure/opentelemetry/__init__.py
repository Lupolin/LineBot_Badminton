from .decorator import trace_method
from .instrumentation import setup_opentelemetry_instrumentor
from .log_factory import otel_trace_record_factory
from .provider import setup_logger_provider, setup_tracer_provider
from .resource import resource
