from typing import Generic, TypeVar

from opentelemetry import trace
from pydantic import BaseModel

T = TypeVar("T")


class ApiResponse(BaseModel, Generic[T]):
    success: bool
    data: T | None = None
    error: str | None = None
    trace_id: str | None = None

    @classmethod
    def success_response(cls, data: T) -> "ApiResponse[T]":
        # 自動抓取目前的 trace_id
        span_context = trace.get_current_span().get_span_context()
        trace_id = format(span_context.trace_id, "032x") if span_context.is_valid else None
        return cls(success=True, data=data, trace_id=trace_id)

    @classmethod
    def error_response(cls, message: str) -> "ApiResponse":
        span_context = trace.get_current_span().get_span_context()
        trace_id = format(span_context.trace_id, "032x") if span_context.is_valid else None
        return cls(success=False, error=message, trace_id=trace_id)
