from fastapi import FastAPI

from api import api_router
from infrastructure.logger import setup_logger
from infrastructure.opentelemetry import (
    setup_logger_provider,
    setup_opentelemetry_instrumentor,
    setup_tracer_provider,
)
from infrastructure.response import global_exception_handler
from lifespan import lifespan


class AppStartup:
    def __init__(self, except_handlers=None):
        setup_tracer_provider()
        setup_logger_provider()
        self.logger = setup_logger()

        self._app: FastAPI = FastAPI(
            title="Badminton Bot API",
            version="1.0.0",
            lifespan=lifespan,
        )

        self._app.add_exception_handler(Exception, global_exception_handler)

        setup_opentelemetry_instrumentor(self._app, excluded_urls=[])

        self._app.include_router(api_router, prefix="/api")

    @property
    def instance(self) -> FastAPI:
        return self._app

    @classmethod
    def boot(cls, except_handlers=None) -> FastAPI:
        return cls(except_handlers).instance


app = AppStartup.boot()
