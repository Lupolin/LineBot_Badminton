from abc import ABC, abstractmethod

from domain.interaction.entities import MemberInfo


class UpdateMemberInfoRepository(ABC):
    @abstractmethod
    def save(self, member: MemberInfo) -> None:
        pass

    @abstractmethod
    def find_by_id(self, user_id: str) -> MemberInfo | None:
        pass
