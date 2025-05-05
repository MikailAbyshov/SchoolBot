from abc import ABC, abstractmethod
from Core.Entities.Teacher import Teacher
from typing import List, Optional

class ITeacherRepository(ABC):
    @abstractmethod
    async def get_all_async(self) -> List[Teacher]:
        pass

    @abstractmethod
    async def get_by_id_async(self, teacher_id: int) -> Optional[Teacher]:
        pass

    @abstractmethod
    async def add_async(self, teacher: Teacher) -> Teacher:
        pass

    @abstractmethod
    async def update_async(self, teacher: Teacher) -> Teacher:
        pass

    @abstractmethod
    async def delete_async(self, teacher_id: int) -> bool:
        pass