from collections.abc import Callable
from dataclasses import (
    dataclass,
    field,
)
from logging import Logger
from zoneinfo import ZoneInfo

from apscheduler.schedulers.asyncio import AsyncIOScheduler


@dataclass
class SchedulerService:
    timezone: str
    logger: Logger
    _scheduler: AsyncIOScheduler = field(init=False)

    def __post_init__(self):
        self._scheduler = AsyncIOScheduler(timezone=ZoneInfo(self.timezone))

    def start(self):
        self.logger.info(f"[Scheduler] Starting background scheduler (Timezone: {self.timezone})")
        self._scheduler.start()
        self.logger.info("[Scheduler] Scheduler service started successfully")

    def add_job(self, func: Callable, *args, **kwargs):
        self._scheduler.add_job(func, *args, **kwargs)

    def stop(self):
        self.logger.info("[Scheduler] Shutting down scheduler service...")
        self._scheduler.shutdown()
