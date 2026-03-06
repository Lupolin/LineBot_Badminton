from dataclasses import dataclass


@dataclass(frozen=True)
class BadmintonSettings:
    location: str = "臺北市信義區信義國民小學"
    time_slot: str = "18:00-20:00"
    day_of_week: str = "friday"

    # 重置回覆狀態時間
    reset_day: str = "sun"
    reset_time: str = "21:00"
