from collections import Counter
from dataclasses import dataclass
from logging import Logger

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from domain.routine.entities import (
    Absentee,
    Attendance,
)
from domain.routine.repository import AttendanceRecordRepository
from infrastructure.opentelemetry import trace_method
from infrastructure.sqlalchemy import SQLAlchemyContext, transaction_scope_async
from infrastructure.sqlalchemy.models import (
    AttendanceRecord,
    MemberProfile,
)


@dataclass
class AttendanceRecordRepositoryImpl(AttendanceRecordRepository):
    session_factory: SQLAlchemyContext
    logger: Logger

    @trace_method("Infra: AttendanceRecordRepository.save_all")
    @transaction_scope_async
    async def save_all(self, session: AsyncSession, records: list[Attendance]) -> None:
        for record in records:
            db_record = AttendanceRecord(
                user_id=record.user_id,
                user_name=record.user_name,
                is_attending=record.is_attending,
                played_date=record.played_date,
            )
            session.add(db_record)

        self.logger.info(f"Successfully saved {len(records)} attendance records")

    @trace_method("Infra: AttendanceRecordRepository.get_all_data")
    @transaction_scope_async
    async def get_all_data(self, session: AsyncSession) -> list[Attendance]:
        stmt = (
            select(MemberProfile)
            .where(MemberProfile.status == "ACTIVE")
        )
        result = await session.execute(stmt)
        db_members = result.scalars().all()

        if not db_members:
            return []

        self.logger.info(f"Successfully retrieved active members for attendance | Count: {len(db_members)}")
        return [
            Attendance(
                user_id=member.user_id,
                user_name=member.user_name,
                is_attending=member.is_attending,
                played_date=member.played_date or "",
            )
            for member in db_members
        ]

    @trace_method("Infra: AttendanceRecordRepository.find_all_data")
    @transaction_scope_async
    async def find_all_data(self, session: AsyncSession) -> list[Attendance] | None:
        stmt = select(AttendanceRecord)
        result = await session.execute(stmt)
        db_records = result.scalars().all()

        self.logger.info(f"Successfully found all historical records | Count: {len(db_records)}")
        return [
            Attendance(
                user_id=record.user_id,
                user_name=record.user_name,
                is_attending=record.is_attending,
                played_date=record.played_date,
            )
            for record in db_records
        ]

    @trace_method("Infra: AttendanceRecordRepository.find_top_absentees")
    @transaction_scope_async
    async def find_top_absentees(self, session: AsyncSession) -> list[Absentee]:
        all_data = await self.find_all_data()

        absent_records = [d for d in all_data if not d.is_attending]
        counts = Counter(record.user_id for record in absent_records)
        top_three = counts.most_common(3)
        user_names = {r.user_id: r.user_name for r in all_data}

        result = [
            Absentee(
                user_name=user_names.get(uid, "Unknown"),
                absent_count=count
            ) for uid, count in top_three
        ]

        self.logger.info(f"Successfully found {len(result)} top absentees.")
        return result
