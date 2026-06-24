from abc import ABC, abstractmethod

from domain.entity import Admin, MemberInfo


class MemberProfileRepository(ABC):
    @abstractmethod
    async def get_pending_members(self) -> list[MemberInfo]:
        pass

    @abstractmethod
    async def get_attending_members(self) -> list[MemberInfo]:
        pass

    @abstractmethod
    async def get_not_attending_members(self) -> list[MemberInfo]:
        pass

    @abstractmethod
    async def get_admin_members(self) -> list[Admin]:
        pass

    @abstractmethod
    async def update_played_date(self, played_date: str) -> None:
        pass

    @abstractmethod
    async def reset_all_attendance(self) -> None:
        pass

    @abstractmethod
    async def save(self, member: MemberInfo) -> None:
        pass

    @abstractmethod
    async def find_by_id(self, user_id: str) -> MemberInfo | None:
        pass
