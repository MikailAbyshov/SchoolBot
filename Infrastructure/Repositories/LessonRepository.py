from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from typing import List
from Core.Interfaces.ILessonRepository import ILessonRepository
from Core.Entities.Lesson import Lesson
from Infrastructure.Dto.LessonDto import LessonDto
from Infrastructure.Mappers.LessonMapper import LessonMapper

class LessonRepository(ILessonRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all_async(self) -> List[Lesson]:
        result = await self.session.execute(select(LessonDto))
        return [LessonMapper.to_entity(dto) for dto in result.scalars()]

    async def get_by_id_async(self, lesson_id: int) -> Lesson:
        result = await self.session.execute(
            select(LessonDto).where(LessonDto.self_id == lesson_id))
        dto = result.scalar_one_or_none()
        return LessonMapper.to_entity(dto) if dto else None

    async def add_async(self, lesson: Lesson) -> Lesson:
        dto = LessonMapper.to_dto(lesson)  # Конвертируем Entity → DTO
        self.session.add(dto)
        await self.session.commit()
        await self.session.refresh(dto)  # Обновляем ID, если он генерируется в БД
        return LessonMapper.to_entity(dto)  # Возвращаем Entity с актуальным ID

    async def update_async(self, lesson: Lesson) -> Lesson:
        if lesson.self_id is None:
            raise ValueError("Lesson ID cannot be None for update")
        dto = LessonMapper.to_dto(lesson)
        await self.session.execute(
            update(LessonDto)
            .where(LessonDto.self_id == dto.self_id)
            .values(
                title=dto.title,
                teacher_id=dto.teacher_id,
                time_slot_id=dto.time_slot_id,
                student_id=dto.student_id
            )
        )
        await self.session.commit()
        return lesson

    async def delete_async(self, lesson_id: int) -> bool:
        # Удаляем урок по ID
        result = await self.session.execute(
            delete(LessonDto)
            .where(LessonDto.self_id == lesson_id)
        )
        await self.session.commit()

        # Возвращаем True, если была удалена хотя бы одна запись
        return result.rowcount > 0

    async def get_lessons_by_time_slots_async(
            self,
            time_slot_ids: List[int]
    ) -> List[Lesson]:
        if not time_slot_ids:
            return []

        result = await self.session.execute(
            select(LessonDto).where(
                LessonDto.time_slot_id.in_(time_slot_ids)
            )
        )
        dtos = result.scalars().all()
        return [LessonMapper.to_entity(dto) for dto in dtos]

    async def get_by_teacher_id_async(self, teacher_id: int) -> List[Lesson]:
        result = await self.session.execute(
            select(LessonDto).where(
                LessonDto.teacher_id == teacher_id
            )
        )
        dtos = result.scalars().all()
        return [LessonMapper.to_entity(dto) for dto in dtos]

    async def get_by_student_id_async(self, student_id: int) -> List[Lesson]:
        result = await self.session.execute(
            select(LessonDto).where(
                LessonDto.student_id == student_id
            )
        )
        dtos = result.scalars().all()
        return [LessonMapper.to_entity(dto) for dto in dtos]

    async def get_lessons_by_student_id_async(self, student_id: int) -> List[Lesson]:
        """
        Возвращает все уроки, связанные с данным student_id.
        """
        stmt = select(LessonDto).where(LessonDto.student_id == student_id)
        result = await self.session.execute(stmt)
        dtos = result.scalars().all()
        return [LessonMapper.to_entity(dto) for dto in dtos]
