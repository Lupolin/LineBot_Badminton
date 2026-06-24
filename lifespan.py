from contextlib import asynccontextmanager

from fastapi import FastAPI

from app import registry as app_registry
from infrastructure import registry as infra_registry


@asynccontextmanager
async def lifespan(app: FastAPI):
    scheduler = infra_registry.scheduler_service

    scheduler.add_job(
        app_registry.send_reminder_use_case.execute,
        "cron",
        day_of_week="mon,tue,wed",
        hour=13,
        minute=0,
        misfire_grace_time=60,  # 允許延遲 60 秒
        id="daily_send_reminder",
    )

    scheduler.add_job(
        app_registry.update_played_date_use_case.execute,
        "cron",
        day_of_week="mon",
        hour=13,
        minute=30,
        misfire_grace_time=60,  # 允許延遲 60 秒
        id="mon_update_played_date",
    )

    scheduler.add_job(
        app_registry.send_summary_use_case.execute,
        "cron",
        day_of_week="wed",
        hour=17,
        minute=0,
        misfire_grace_time=60,  # 允許延遲 60 秒
        id="wed_send_summary",
    )

    scheduler.add_job(
        app_registry.reset_attendance_use_case.execute,
        "cron",
        day_of_week="fri",
        hour=20,
        minute=10,
        misfire_grace_time=60,  # 允許延遲 60 秒
        id="sun_reset_attendance",
    )

    scheduler.add_job(
        app_registry.insert_attendance_record_use_case.execute,
        "cron",
        day_of_week="fri",
        hour=20,
        minute=0,
        misfire_grace_time=60,  # 允許延遲 60 秒
        id="fri_insert_attendance_record",
    )

    scheduler.start()

    try:
        yield
    finally:
        scheduler.stop()
