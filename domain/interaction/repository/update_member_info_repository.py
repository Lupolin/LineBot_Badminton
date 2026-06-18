from abc import ABC, abstractmethod

from domain.interaction.entities import MemberInfo


class UpdateMemberInfoRepository(ABC):
    @abstractmethod
    async def save(self, member: MemberInfo) -> None:
        pass

    @abstractmethod
    async def find_by_id(self, user_id: str) -> MemberInfo | None:
        pass
