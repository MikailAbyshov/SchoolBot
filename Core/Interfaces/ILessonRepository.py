from abc import ABC, abstractmethod
from Core.Entities.Lesson import Lesson
from typing import List, Optional

class ILessonRepository(ABC):
    @abstractmethod
    async def get_all_async(self) -> List[Lesson]:
        pass

    @abstractmethod
    async def get_by_id_async(self, lesson_id: int) -> Optional[Lesson]:
        pass

    @abstractmethod
    async def add_async(self, lesson: Lesson) -> Lesson:
        pass

    @abstractmethod
    async def update_async(self, lesson: Lesson) -> Lesson:
        pass

    @abstractmethod
    async def delete_async(self, lesson_id: int) -> bool:
        pass

    @abstractmethod
    async def get_by_teacher_id_async(self, teacher_id: int) -> List[Lesson]:
        pass

    @abstractmethod
    async def get_by_student_id_async(self, student_id: int) -> List[Lesson]:
        pass

    @abstractmethod
    async def get_lessons_by_time_slots_async(
            self,
            time_slot_ids: List[int]
    ) -> List[Lesson]:
        """Возвращает уроки, связанные с указанными слотами."""
        pass

    @abstractmethod
    async def get_lessons_by_student_id_async(self, student_id: int) -> List[Lesson]:
        pass