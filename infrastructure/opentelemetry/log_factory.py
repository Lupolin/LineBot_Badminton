import logging

from opentelemetry import trace

old_factory = logging.getLogRecordFactory()


def otel_trace_record_factory(*args, **kwargs):
    """
    reference : https://github.com/open-telemetry/opentelemetry-python-contrib/blob/main/instrumentation/opentelemetry-instrumentation-logging/src/opentelemetry/instrumentation/logging/__init__.py#L125
    """

    record = old_factory(*args, **kwargs)

    record.otelSpanID = "0"
    record.otelTraceID = "0"

    span = trace.get_current_span()
    ctx = span.get_span_context()

    if ctx.is_valid:
        record.otelSpanID = format(ctx.span_id, "016x")
        record.otelTraceID = format(ctx.trace_id, "032x")

    return record
