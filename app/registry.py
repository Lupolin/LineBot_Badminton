import logging

from app.interaction import IntentDispatcher
from app.interaction.usecases import (
    HandleAttendanceUseCase,
    NotifyAgainUseCase,
    QueryStatUseCase,
    RegisterMemberUseCase,
)
from app.routine import (
    InsertAttendanceRecordUseCase,
    ResetAttendanceUseCase,
    SendReminderUseCase,
    SendSummaryUseCase,
    UpdatePlayedDateUseCase,
)
from domain.interaction.entities import UserIntent
from domain.routine import (
    BadmintonMessages,
    MessageService,
)
from infrastructure.common.impl import (
    DateTimeCalendarServiceImpl,
    LineApiServiceImpl,
    LineMessageHandlerImpl,
    LineMessageServiceImpl,
)
from infrastructure.scheduler import SchedulerService
from infrastructure.setting.config import config as cfg
from infrastructure.sqlalchemy import SQLAlchemyContext
from infrastructure.sqlalchemy.repositories import (
    AttendanceRecordRepositoryImpl,
    MemberRepositoryImpl,
)


class Registry:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.session_factory = SQLAlchemyContext(logger=self.logger)
        self.scheduler_service = SchedulerService(logger=self.logger)
        self.line_api_service = LineApiServiceImpl(logger=self.logger)
        self.line_message_handler = LineMessageHandlerImpl(logger=self.logger)
        self._member_repo = MemberRepositoryImpl(
            session_factory=self.session_factory,
            logger=self.logger,
        )
        self._record_repo = AttendanceRecordRepositoryImpl(
            session_factory=self.session_factory,
            logger=self.logger,
        )
        self._messenger = LineMessageServiceImpl(
            access_token=cfg.LINE_BOT.CHANNEL_ACCESS_TOKEN,
            logger=self.logger,
        )
        self._msg_service = MessageService(
            messages=BadmintonMessages(),
            timezone=cfg.TIMEZONE,
        )
        self._calendar = DateTimeCalendarServiceImpl(logger=self.logger)
        self._use_case_map = {
            UserIntent.ATTEND: lambda: self.handle_attendance_use_case,
            UserIntent.CANCEL: lambda: self.handle_attendance_use_case,
            UserIntent.REGISTER: lambda: self.register_member_use_case,
            UserIntent.QUERY_STAT: lambda: self.query_stat_use_case,
            UserIntent.NOTIFY_AGAIN: lambda: self.notify_again_use_case,
        }

    @property
    def send_reminder_use_case(self) -> SendReminderUseCase:
        return SendReminderUseCase(
            repo=self._member_repo,
            messenger=self._messenger,
            provider=self._msg_service,
            calendar=self._calendar,
            logger=self.logger,
        )

    @property
    def send_summary_use_case(self) -> SendSummaryUseCase:
        return SendSummaryUseCase(
            repo=self._member_repo,
            messenger=self._messenger,
            provider=self._msg_service,
            calendar=self._calendar,
            logger=self.logger,
        )

    @property
    def reset_attendance_use_case(self) -> ResetAttendanceUseCase:
        return ResetAttendanceUseCase(
            repo=self._member_repo,
            logger=self.logger,
        )

    @property
    def update_played_date_use_case(self) -> UpdatePlayedDateUseCase:
        return UpdatePlayedDateUseCase(
            repo=self._member_repo,
            calendar=self._calendar,
            logger=self.logger,
        )

    @property
    def insert_attendance_record_use_case(self) -> InsertAttendanceRecordUseCase:
        return InsertAttendanceRecordUseCase(
            repo=self._record_repo,
            logger=self.logger,
        )

    @property
    def dispatcher(self) -> IntentDispatcher:
        return IntentDispatcher(
            registry=self,
            member_repo=self._member_repo,
            messenger=self._messenger,
        )

    @property
    def handle_attendance_use_case(self) -> HandleAttendanceUseCase:
        return HandleAttendanceUseCase(
            member_repo=self._member_repo,
            logger=self.logger,
        )

    @property
    def register_member_use_case(self) -> RegisterMemberUseCase:
        return RegisterMemberUseCase(
            member_repo=self._member_repo,
            messenger=self._messenger,
            line_api_service=self.line_api_service,
            logger=self.logger,
        )

    @property
    def query_stat_use_case(self) -> QueryStatUseCase:
        return QueryStatUseCase(
            member_repo=self._member_repo,
            message_repo=self._member_repo,
            messenger=self._messenger,
            provider=self._msg_service,
            calendar=self._calendar,
            logger=self.logger,
        )

    @property
    def notify_again_use_case(self) -> NotifyAgainUseCase:
        return NotifyAgainUseCase(
            member_repo=self._member_repo,
            message_repo=self._member_repo,
            messenger=self._messenger,
            provider=self._msg_service,
            calendar=self._calendar,
            logger=self.logger,
        )

    def get_use_case_by_intent(self, intent: UserIntent):
        use_case = self._use_case_map.get(intent)

        if use_case:
            return use_case()
        return None


registry = Registry()
