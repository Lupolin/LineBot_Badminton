from logging import Logger

import pytz
from apscheduler.schedulers.background import BackgroundScheduler

from infrastructure.setting import config

from .factory import SchedulerFactory


class SchedulerService:
    def __init__(
        self,
        logger: Logger,
    ):
        self._scheduler = BackgroundScheduler(timezone=pytz.timezone(config.TIMEZONE))
        self.logger = logger

    def start(self):
        self.logger.info(f"[Scheduler] Starting background scheduler (Timezone: {config.TIMEZONE})")

        self._scheduler.add_job(
            lambda: SchedulerFactory.send_reminder().execute(),
            "cron",
            day_of_week="mon,tue,wed",
            hour=13,
            minute=0,
            id="daily_send_reminder",
        )

        self._scheduler.add_job(
            lambda: SchedulerFactory.update_played_date().execute(),
            "cron",
            day_of_week="mon",
            hour=13,
            minute=0,
            id="mon_update_played_date",
        )

        self._scheduler.add_job(
            lambda: SchedulerFactory.send_summary().execute(),
            "cron",
            day_of_week="wed",
            hour=17,
            minute=0,
            id="wed_send_summary",
        )

        self._scheduler.add_job(
            lambda: SchedulerFactory.reset_attendance().execute(),
            "cron",
            day_of_week="fri",
            hour=20,
            minute=0,
            id="sun_reset_attendance",
        )

        self._scheduler.add_job(
            lambda: SchedulerFactory.insert_attendance_record().execute(),
            "cron",
            day_of_week="fri",
            hour=20,
            minute=0,
            id="fri_insert_attendance_record",
        )

        self._scheduler.start()
        self.logger.info("[Scheduler] Scheduler service started successfully.")

    def stop(self):
        self.logger.info("[Scheduler] Shutting down scheduler service...")
        self._scheduler.shutdown()
