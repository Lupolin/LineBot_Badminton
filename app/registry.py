from functools import cached_property

from app.interaction import IntentDispatcher
from app.interaction.use_cases import (
    HandleAttendanceUseCase,
    NotifyAgainUseCase,
    QueryStatUseCase,
    RegisterMemberUseCase,
    SendTopAbsenteeUseCase,
)
from app.routine import (
    FindAttendanceRecordUseCase,
    FindTopAbsenteesUseCase,
    InsertAttendanceRecordUseCase,
    ResetAttendanceUseCase,
    SendReminderUseCase,
    SendSummaryUseCase,
    UpdatePlayedDateUseCase,
)
from domain.entity import BadmintonMessages, UserIntent
from domain.service import MessageGenerator
from infrastructure import registry as infra_registry


class Registry:
    def __init__(self):
        self._message_generator = MessageGenerator(messages=BadmintonMessages())
        self._use_case_map = {
            UserIntent.ATTEND: lambda: self.handle_attendance_use_case,
            UserIntent.CANCEL: lambda: self.handle_attendance_use_case,
            UserIntent.REGISTER: lambda: self.register_member_use_case,
            UserIntent.QUERY_STAT: lambda: self.query_stat_use_case,
            UserIntent.NOTIFY_AGAIN: lambda: self.notify_again_use_case,
            UserIntent.ABSENTEE: lambda: self.send_top_absentee_use_case,
        }

    @property
    def send_reminder_use_case(self) -> SendReminderUseCase:
        return SendReminderUseCase(
            member_profile_repo=infra_registry.member_profile_repo,
            message_service=infra_registry.line_message_service,
            message_generator=self._message_generator,
            calendar=infra_registry.datetime_calendar_service,
            logger=infra_registry.logger,
        )

    @property
    def send_summary_use_case(self) -> SendSummaryUseCase:
        return SendSummaryUseCase(
            member_profile_repo=infra_registry.member_profile_repo,
            message_service=infra_registry.line_message_service,
            message_generator=self._message_generator,
            calendar=infra_registry.datetime_calendar_service,
            logger=infra_registry.logger,
        )

    @property
    def reset_attendance_use_case(self) -> ResetAttendanceUseCase:
        return ResetAttendanceUseCase(
            member_profile_repo=infra_registry.member_profile_repo,
            logger=infra_registry.logger,
        )

    @property
    def update_played_date_use_case(self) -> UpdatePlayedDateUseCase:
        return UpdatePlayedDateUseCase(
            member_profile_repo=infra_registry.member_profile_repo,
            calendar=infra_registry.datetime_calendar_service,
            logger=infra_registry.logger,
        )

    @property
    def insert_attendance_record_use_case(self) -> InsertAttendanceRecordUseCase:
        return InsertAttendanceRecordUseCase(
            attendance_record_repo=infra_registry.attendance_record_repo,
            logger=infra_registry.logger,
        )

    @property
    def find_top_absentees_use_case(self) -> FindTopAbsenteesUseCase:
        return FindTopAbsenteesUseCase(
            attendance_record_repo=infra_registry.attendance_record_repo,
            logger=infra_registry.logger,
        )

    @property
    def find_attendance_record_use_case(self) -> FindAttendanceRecordUseCase:
        return FindAttendanceRecordUseCase(
            attendance_record_repo=infra_registry.attendance_record_repo,
            logger=infra_registry.logger,
        )

    @cached_property
    def dispatcher(self) -> IntentDispatcher:
        return IntentDispatcher(
            registry=self,
            member_profile_repo=infra_registry.member_profile_repo,
            message_service=infra_registry.line_message_service,
            logger=infra_registry.logger,
        )

    @property
    def handle_attendance_use_case(self) -> HandleAttendanceUseCase:
        return HandleAttendanceUseCase(
            member_profile_repo=infra_registry.member_profile_repo,
            logger=infra_registry.logger,
        )

    @property
    def register_member_use_case(self) -> RegisterMemberUseCase:
        return RegisterMemberUseCase(
            member_profile_repo=infra_registry.member_profile_repo,
            message_service=infra_registry.line_message_service,
            api_service=infra_registry.line_api_service,
            logger=infra_registry.logger,
        )

    @property
    def query_stat_use_case(self) -> QueryStatUseCase:
        return QueryStatUseCase(
            member_profile_repo=infra_registry.member_profile_repo,
            message_service=infra_registry.line_message_service,
            message_generator=self._message_generator,
            calendar=infra_registry.datetime_calendar_service,
            logger=infra_registry.logger,
        )

    @property
    def notify_again_use_case(self) -> NotifyAgainUseCase:
        return NotifyAgainUseCase(
            member_profile_repo=infra_registry.member_profile_repo,
            message_service=infra_registry.line_message_service,
            message_generator=self._message_generator,
            calendar=infra_registry.datetime_calendar_service,
            logger=infra_registry.logger,
        )

    @property
    def send_top_absentee_use_case(self) -> SendTopAbsenteeUseCase:
        return SendTopAbsenteeUseCase(
            member_profile_repo=infra_registry.member_profile_repo,
            attendance_record_repo=infra_registry.attendance_record_repo,
            message_service=infra_registry.line_message_service,
            message_generator=self._message_generator,
            logger=infra_registry.logger,
        )

    def get_use_case_by_intent(self, intent: UserIntent):
        use_case = self._use_case_map.get(intent)

        if use_case:
            return use_case()
        return None
