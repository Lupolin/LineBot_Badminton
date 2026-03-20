from logging import Logger

from domain.interaction.entities import MemberInfo
from domain.interaction.repository import UpdateMemberInfoRepository
from domain.routine.entities import Admin, Member
from domain.routine.repository import GetMemberInfoRepository
from infrastructure.opentelemetry import trace_method
from infrastructure.sqlalchemy import SQLAlchemyContext
from infrastructure.sqlalchemy.models import MemberProfile


class MemberRepositoryImpl(
    GetMemberInfoRepository,
    UpdateMemberInfoRepository,
):
    def __init__(
        self,
        session_factory: SQLAlchemyContext,
        logger: Logger,
    ):
        self.session_factory = session_factory
        self.logger = logger

    @trace_method("Infra: MemberRepository.get_pending_members")
    def get_pending_members(self) -> list[Member]:
        with self.session_factory.begin() as session:
            members = (
                session.query(MemberProfile)
                .filter(
                    MemberProfile.is_attending.is_(None),
                )
                .all()
            )
            return [
                Member(
                    user_id=m.user_id,
                    user_name=m.user_name,
                    is_attending=True,
                    played_date=m.played_date,
                )
                for m in members
            ]

    @trace_method("Infra: MemberRepository.get_attending_members")
    def get_attending_members(self) -> list[Member]:
        with self.session_factory.begin() as session:
            members = (
                session.query(MemberProfile)
                .filter(
                    MemberProfile.last_replied_at.isnot(None),
                    MemberProfile.is_attending.is_(True),
                )
                .all()
            )
            return [
                Member(
                    user_id=m.user_id,
                    user_name=m.user_name,
                    is_attending=True,
                    played_date=m.played_date,
                )
                for m in members
            ]

    @trace_method("Infra: MemberRepository.get_not_attending_members")
    def get_not_attending_members(self) -> list[Member]:
        with self.session_factory.begin() as session:
            members = (
                session.query(MemberProfile)
                .filter(MemberProfile.last_replied_at.isnot(None), MemberProfile.is_attending.is_(False))
                .all()
            )
            return [
                Member(
                    user_id=m.user_id,
                    user_name=m.user_name,
                    is_attending=False,
                    played_date=m.played_date,
                )
                for m in members
            ]

    @trace_method("Infra: MemberRepository.get_admin_members")
    def get_admin_members(self) -> list[Admin]:
        with self.session_factory.begin() as session:
            members = (
                session.query(MemberProfile)
                .filter(
                    MemberProfile.role == "Admin",
                )
                .all()
            )
            # 轉化為 Domain Entity: Admin
            return [
                Admin(
                    user_id=m.user_id,
                    user_role=m.role,
                )
                for m in members
            ]

    @trace_method("Infra: MemberRepository.get_all_members")
    def get_all_members(self) -> list[Member]:
        with self.session_factory.begin() as session:
            members = session.query(MemberProfile).all()
            return [
                Member(
                    user_id=m.user_id,
                    user_name=m.user_name,
                    is_attending=m.is_attending,
                    played_date=m.played_date,
                )
                for m in members
            ]

    @trace_method("Infra: MemberRepository.reset_played_date")
    def update_played_date(self, played_date: str) -> None:
        with self.session_factory.begin() as session:
            session.query(MemberProfile).update(
                {
                    MemberProfile.played_date: played_date,
                }
            )
        return None

    @trace_method("Infra: MemberRepository.reset_all_attendance")
    def reset_all_attendance(self) -> None:
        with self.session_factory.begin() as session:
            session.query(MemberProfile).update(
                {
                    MemberProfile.is_attending: None,
                    MemberProfile.last_replied_at: None,
                    MemberProfile.played_date: None,
                }
            )
        return None

    @trace_method("Infra: MemberRepository.save")
    def save(self, member: MemberInfo) -> None:
        try:
            with self.session_factory.begin() as session:
                db_member = session.query(MemberProfile).filter(MemberProfile.user_id == member.user_id).first()

                if db_member:
                    db_member.user_name = member.user_name
                    db_member.role = member.role
                    db_member.intent = member.intent
                    db_member.is_attending = member.is_attending
                    db_member.user_content = member.user_content
                    db_member.last_replied_at = member.last_replied_at
                else:
                    db_member = MemberProfile(
                        user_id=member.user_id,
                        user_name=member.user_name,
                        role=member.role,
                        intent=member.intent,
                        is_attending=member.is_attending,
                        user_content=member.user_content,
                        last_replied_at=member.last_replied_at,
                    )
                    session.add(db_member)
            self.logger.info(f"Successfully saved member info for {member.user_id}")
        except Exception as e:
            raise RuntimeError(f"Error saving member info for {member.user_id}") from e

    @trace_method("Infra: MemberRepository.find_by_id")
    def find_by_id(self, user_id: str) -> MemberInfo | None:
        with self.session_factory.begin() as session:
            db_member = session.query(MemberProfile).filter(MemberProfile.user_id == user_id).first()
            if db_member is None:
                return None

            return MemberInfo(
                user_id=db_member.user_id,
                user_name=db_member.user_name,
                role=db_member.role,
                is_attending=db_member.is_attending,
                user_content=db_member.user_content,
                intent=db_member.intent,
                last_replied_at=db_member.last_replied_at,
            )
