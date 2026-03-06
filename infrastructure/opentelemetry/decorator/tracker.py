from functools import wraps

from opentelemetry import trace


def trace_method(name: str | None = None):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            tracer = trace.get_tracer(__name__)
            span_name = name or f"Method: {func.__name__}"
            with tracer.start_as_current_span(span_name):
                return func(*args, **kwargs)

        return wrapper

    return decorator
