from logging import Logger

from infrastructure.sqlalchemy.models import AttendanceRecord
from domain.routine.entities import Attendance
from domain.routine.repository import AttendanceRecordRepository
from infrastructure.opentelemetry import trace_method
from infrastructure.sqlalchemy import SQLAlchemyContext
from infrastructure.sqlalchemy.models import MemberProfile


class AttendanceRecordRepositoryImpl(AttendanceRecordRepository):
    def __init__(
        self,
        session_factory: SQLAlchemyContext,
        logger: Logger,
    ):
        self.session_factory = session_factory
        self.logger = logger

    @trace_method("Infra: AttendanceRecordRepository.save_all")
    def save_all(self, records: list[Attendance]) -> None:
        try:
            with self.session_factory.begin() as session:
                for record in records:
                    db_record = AttendanceRecord(
                        user_id=record.user_id,
                        user_name=record.user_name,
                        is_attending=record.is_attending,
                        played_date=record.played_date,
                    )
                    session.add(db_record)

            self.logger.info("Successfully saved Record.")
        except Exception as e:
            raise ValueError("Failed to save attendance records") from e

    @trace_method("Infra: AttendanceRecordRepository.get_all_data")
    def get_all_data(self) -> list[Attendance] | None:
        with self.session_factory.begin() as session:
            db_members = session.query(MemberProfile).all()
            if not db_members:
                return []

            return [
                Attendance(
                    user_id=member.user_id,
                    user_name=member.user_name,
                    is_attending=member.is_attending,
                    played_date=member.played_date,
                )
                for member in db_members
            ]
