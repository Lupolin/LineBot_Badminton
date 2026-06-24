from fastapi import FastAPI
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor


def setup_opentelemetry_instrumentor(app: FastAPI, excluded_urls: list[str]):
    FastAPIInstrumentor.instrument_app(
        app,
        excluded_urls=",".join(excluded_urls) if excluded_urls else None,
        exclude_spans=["receive", "send"],
    )
