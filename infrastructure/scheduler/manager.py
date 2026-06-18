from dataclasses import (
    dataclass,
    field,
)
from logging import Logger
from zoneinfo import ZoneInfo

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from infrastructure.setting import config

from .factory import SchedulerFactory


@dataclass
class SchedulerService:
    logger: Logger
    _scheduler: AsyncIOScheduler = field(init=False)

    def __post_init__(self):
        self._scheduler = AsyncIOScheduler(timezone=ZoneInfo(config.TIMEZONE))

    def start(self):
        self.logger.info(f"[Scheduler] Starting background scheduler (Timezone: {config.TIMEZONE})")

        self._scheduler.add_job(
            SchedulerFactory.send_reminder().execute,
            "cron",
            day_of_week="mon,tue,wed",
            hour=13,
            minute=0,
            misfire_grace_time=60,  # 允許延遲 60 秒
            id="daily_send_reminder",
        )

        self._scheduler.add_job(
            SchedulerFactory.update_played_date().execute,
            "cron",
            day_of_week="mon",
            hour=13,
            minute=30,
            misfire_grace_time=60,  # 允許延遲 60 秒
            id="mon_update_played_date",
        )

        self._scheduler.add_job(
            SchedulerFactory.send_summary().execute,
            "cron",
            day_of_week="wed",
            hour=17,
            minute=0,
            misfire_grace_time=60,  # 允許延遲 60 秒
            id="wed_send_summary",
        )

        self._scheduler.add_job(
            SchedulerFactory.reset_attendance().execute,
            "cron",
            day_of_week="fri",
            hour=20,
            minute=10,
            misfire_grace_time=60,  # 允許延遲 60 秒
            id="sun_reset_attendance",
        )

        self._scheduler.add_job(
            SchedulerFactory.insert_attendance_record().execute,
            "cron",
            day_of_week="fri",
            hour=20,
            minute=0,
            misfire_grace_time=60,  # 允許延遲 60 秒
            id="fri_insert_attendance_record",
        )

        self._scheduler.start()
        self.logger.info("[Scheduler] Scheduler service started successfully")

    def stop(self):
        self.logger.info("[Scheduler] Shutting down scheduler service...")
        self._scheduler.shutdown()
