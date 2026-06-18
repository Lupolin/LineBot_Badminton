import asyncio
from functools import wraps

from opentelemetry import trace


def trace_method(name: str | None = None):
    def decorator(func):
        if asyncio.iscoroutinefunction(func):

            @wraps(func)
            async def async_wrapper(*args, **kwargs):
                tracer = trace.get_tracer(__name__)
                span_name = name or f"Method: {func.__name__}"
                with tracer.start_as_current_span(span_name):
                    return await func(*args, **kwargs)

            return async_wrapper
        else:

            @wraps(func)
            def sync_wrapper(*args, **kwargs):
                tracer = trace.get_tracer(__name__)
                span_name = name or f"Method: {func.__name__}"
                with tracer.start_as_current_span(span_name):
                    return func(*args, **kwargs)  # 同步直接執行

            return sync_wrapper

    return decorator
