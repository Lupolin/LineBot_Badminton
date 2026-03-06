from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.registry import registry


@asynccontextmanager
async def lifespan(app: FastAPI):
    registry.session_factory.init_db()
    registry.scheduler_service.start()

    app.state.scheduler = registry.scheduler_service

    try:
        yield
    finally:
        registry.scheduler_service.stop()
