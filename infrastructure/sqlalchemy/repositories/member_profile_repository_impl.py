from dataclasses import dataclass
from logging import Logger

from sqlalchemy import (
    select,
    update,
)
from sqlalchemy.ext.asyncio import AsyncSession

from domain.entity import Admin, MemberInfo
from domain.repository import MemberProfileRepository
from infrastructure.opentelemetry import trace_method
from infrastructure.sqlalchemy import SQLAlchemyContext, transaction_scope_async
from infrastructure.sqlalchemy.models import MemberProfile


@dataclass
class MemberRepositoryImpl(MemberProfileRepository):
    session_factory: SQLAlchemyContext
    logger: Logger

    @trace_method("Infra: MemberRepository.get_pending_members")
    @transaction_scope_async
    async def get_pending_members(self, session: AsyncSession) -> list[MemberInfo]:
        stmt = select(MemberProfile).where(
            MemberProfile.is_attending.is_(None),
            MemberProfile.status == "ACTIVE",
        )
        result = await session.execute(stmt)
        members = result.scalars().all()

        self.logger.info(f"Retrieved pending members | Count: {len(members)}")

        return [
            MemberInfo(
                user_id=m.user_id,
                user_name=m.user_name,
                user_content=m.user_content,
                is_attending=m.is_attending,
            )
            for m in members
        ]

    @trace_method("Infra: MemberRepository.get_attending_members")
    @transaction_scope_async
    async def get_attending_members(self, session: AsyncSession) -> list[MemberInfo]:
        stmt = select(MemberProfile).where(
            MemberProfile.last_replied_at.isnot(None),
            MemberProfile.is_attending.is_(True),
            MemberProfile.status == "ACTIVE",
        )
        result = await session.execute(stmt)
        members = result.scalars().all()

        self.logger.info(f"Retrieved attending members | Count: {len(members)}")

        return [
            MemberInfo(
                user_id=m.user_id,
                user_name=m.user_name,
                user_content=m.user_content,
                is_attending=m.is_attending,
            )
            for m in members
        ]

    @trace_method("Infra: MemberRepository.get_not_attending_members")
    @transaction_scope_async
    async def get_not_attending_members(self, session: AsyncSession) -> list[MemberInfo]:
        stmt = select(MemberProfile).where(
            MemberProfile.last_replied_at.isnot(None),
            MemberProfile.is_attending.is_(False),
            MemberProfile.status == "ACTIVE",
        )
        result = await session.execute(stmt)
        members = result.scalars().all()

        self.logger.info(f"Retrieved not attending members | Count: {len(members)}")

        return [
            MemberInfo(
                user_id=m.user_id,
                user_name=m.user_name,
                user_content=m.user_content,
                is_attending=m.is_attending,
            )
            for m in members
        ]

    @trace_method("Infra: MemberRepository.get_admin_members")
    @transaction_scope_async
    async def get_admin_members(self, session: AsyncSession) -> list[Admin]:
        stmt = select(MemberProfile).where(
            MemberProfile.role == "Admin",
            MemberProfile.status == "ACTIVE",
        )
        result = await session.execute(stmt)
        members = result.scalars().all()

        self.logger.info(f"Retrieved admin members | Count: {len(members)}")

        return [
            Admin(
                user_id=m.user_id,
                user_role=m.role,
            )
            for m in members
        ]

    @trace_method("Infra: MemberRepository.update_played_date")
    @transaction_scope_async
    async def update_played_date(self, session: AsyncSession, played_date: str) -> None:
        stmt = update(MemberProfile).values(played_date=played_date).returning(MemberProfile.id)
        result = await session.execute(stmt)
        affected_rows = result.scalars().all()

        self.logger.info(f"Updated played date [{played_date}] | Affected rows [{len(affected_rows)}]")

        return None

    @trace_method("Infra: MemberRepository.reset_all_attendance")
    @transaction_scope_async
    async def reset_all_attendance(self, session: AsyncSession) -> None:
        stmt = (
            update(MemberProfile)
            .values(
                is_attending=None,
                last_replied_at=None,
                played_date=None,
            )
            .returning(MemberProfile.id)
        )
        result = await session.execute(stmt)
        affected_rows = result.scalars().all()

        self.logger.info(f"Reset attendance for all members | Affected rows [{len(affected_rows)}]")

        return None

    @trace_method("Infra: MemberRepository.save")
    @transaction_scope_async
    async def save(self, session: AsyncSession, member: MemberInfo) -> None:
        stmt = select(MemberProfile).where(MemberProfile.user_id == member.user_id)
        result = await session.execute(stmt)
        db_member = result.scalar_one_or_none()

        if db_member:
            db_member.user_name = member.user_name
            db_member.role = member.role
            db_member.status = member.status
            db_member.intent = member.intent
            db_member.is_attending = member.is_attending
            db_member.user_content = member.user_content
            db_member.last_replied_at = member.last_replied_at
        else:
            db_member = MemberProfile(
                user_id=member.user_id,
                user_name=member.user_name,
                role=member.role,
                status=member.status,
                intent=member.intent,
                is_attending=member.is_attending,
                user_content=member.user_content,
                last_replied_at=member.last_replied_at,
            )
            session.add(db_member)

        self.logger.info(f"Successfully saved member info for {member.user_id}")

    @trace_method("Infra: MemberRepository.find_by_id")
    @transaction_scope_async
    async def find_by_id(self, session: AsyncSession, user_id: str) -> MemberInfo | None:
        stmt = select(MemberProfile).where(MemberProfile.user_id == user_id)
        result = await session.execute(stmt)
        db_member = result.scalar_one_or_none()

        if db_member is None:
            self.logger.warning(f"No member found with user_id: {user_id}")
            return None

        self.logger.info(f"Successfully retrieved member: {user_id} ({db_member.user_name})")

        return MemberInfo(
            user_id=db_member.user_id,
            user_name=db_member.user_name,
            role=db_member.role,
            status=db_member.status,
            is_attending=db_member.is_attending,
            user_content=db_member.user_content,
            intent=db_member.intent,
            last_replied_at=db_member.last_replied_at,
        )
