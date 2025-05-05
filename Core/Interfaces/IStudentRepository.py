from abc import ABC, abstractmethod
from Core.Entities.Student import Student
from typing import List, Optional

class IStudentRepository(ABC):
    @abstractmethod
    async def get_all_async(self) -> List[Student]:
        pass

    @abstractmethod
    async def get_by_id_async(self, student_id: int) -> Optional[Student]:
        pass

    @abstractmethod
    async def add_async(self, student: Student) -> Student:
        pass

    @abstractmethod
    async def update_async(self, student: Student) -> Student:
        pass

    @abstractmethod
    async def delete_async(self, student_id: int) -> bool:
        pass

    @abstractmethod
    async def get_by_student_contact_async(self, student_contact: str) -> Optional[Student]:
        pass

    @abstractmethod
    async def get_by_parent_contact_async(self, parent_contact: str) -> List[Student]:
        pass
