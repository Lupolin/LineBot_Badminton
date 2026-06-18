"""
log record factory會在log record產生時標記上trace/span id，搭配formatter將trace資訊記錄下來
此factory是為了console/sidecar handler在紀錄log時能夠跟trace/span關聯所用
可參考infrastructure.logger.formatter

但因opentelemetry的log sdk本身在傳送log時會自動偵測當前span的trace/span id，不需特別透過此factory與formatter，
trace資訊也會自動帶入到metadata post到支援otlp的server，因此未來若確認不需要在server本機上紀錄log時，可以考慮拿掉此功能
"""

import logging

from opentelemetry import trace

old_factory = logging.getLogRecordFactory()


def otel_trace_record_factory(*args, **kwargs):
    """
    reference : https://github.com/open-telemetry/opentelemetry-python-contrib/blob/main/instrumentation/opentelemetry-instrumentation-logging/src/opentelemetry/instrumentation/logging/__init__.py#L125
    """

    record = old_factory(*args, **kwargs)

    # 初始化預設值
    record.otelSpanID = "0"
    record.otelTraceID = "0"

    span = trace.get_current_span()
    ctx = span.get_span_context()

    # --- Debug Line: 啟動後在 Terminal 看到這個 print 嗎？ ---
    # print(f"DEBUG: Factory caught SpanID: {ctx.span_id}, Valid: {ctx.is_valid}")

    if ctx.is_valid:
        record.otelSpanID = format(ctx.span_id, "016x")
        record.otelTraceID = format(ctx.trace_id, "032x")

    return record
