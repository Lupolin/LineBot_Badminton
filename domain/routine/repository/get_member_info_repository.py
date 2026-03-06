from abc import ABC, abstractmethod

from domain.routine.entities import Admin, Member


class GetMemberInfoRepository(ABC):
    @abstractmethod
    def get_pending_members(self) -> list[Member]:
        pass

    @abstractmethod
    def get_attending_members(self) -> list[Member]:
        pass

    @abstractmethod
    def get_not_attending_members(self) -> list[Member]:
        pass

    @abstractmethod
    def get_admin_members(self) -> list[Admin]:
        pass

    @abstractmethod
    def get_all_members(self) -> list[Member]:
        pass

    @abstractmethod
    def update_played_date(self, played_date: str) -> None:
        pass

    @abstractmethod
    def reset_all_attendance(self) -> None:
        pass
