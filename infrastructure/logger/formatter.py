import logging
from logging import Formatter


class OpenTelemetryFormatter(Formatter):
    BASE_FORMAT = "[%(levelname)s] [%(asctime)s] \n| %(message)s"
    TRACE_INFO = "\n| trace_id=%(otelTraceID)s\n| span_id=%(otelSpanID)s"

    def format(self, record: logging.LogRecord) -> str:
        trace_id = getattr(record, "otelTraceID", "0")

        self._style._fmt = self.BASE_FORMAT

        if trace_id and trace_id != "0":
            self._style._fmt += self.TRACE_INFO

        return super().format(record)


formatter_with_level: Formatter = OpenTelemetryFormatter(datefmt="%Y-%m-%d %H:%M:%S")

formatter: Formatter = formatter_with_level
