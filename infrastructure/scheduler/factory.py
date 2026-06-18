from app.routine import (
    InsertAttendanceRecordUseCase,
    ResetAttendanceUseCase,
    SendReminderUseCase,
    SendSummaryUseCase,
    UpdatePlayedDateUseCase,
)


class SchedulerFactory:
    @staticmethod
    def send_reminder() -> SendReminderUseCase:
        from app.registry import registry

        return registry.send_reminder_use_case

    @staticmethod
    def send_summary() -> SendSummaryUseCase:
        from app.registry import registry

        return registry.send_summary_use_case

    @staticmethod
    def reset_attendance() -> ResetAttendanceUseCase:
        from app.registry import registry

        return registry.reset_attendance_use_case

    @staticmethod
    def update_played_date() -> UpdatePlayedDateUseCase:
        from app.registry import registry

        return registry.update_played_date_use_case

    @staticmethod
    def insert_attendance_record() -> InsertAttendanceRecordUseCase:
        from app.registry import registry

        return registry.insert_attendance_record_use_case
