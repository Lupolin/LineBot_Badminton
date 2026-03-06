from fastapi import FastAPI
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor


def setup_opentelemetry_instrumentor(app: FastAPI, excluded_urls: list[str] | None = None):
    FastAPIInstrumentor.instrument_app(app, exclude_spans=["receive", "send"])
