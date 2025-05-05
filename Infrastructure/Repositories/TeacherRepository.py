from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from typing import List, Optional
from Core.Entities.Teacher import Teacher
from Core.Interfaces.ITeacherRepository import ITeacherRepository
from Infrastructure.Dto.TeacherDto import TeacherDto
from Infrastructure.Mappers.TeacherMapper import TeacherMapper

class TeacherRepository(ITeacherRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all_async(self) -> List[Teacher]:
        result = await self.session.execute(select(TeacherDto))
        return [TeacherMapper.to_entity(dto) for dto in result.scalars()]

    async def get_by_id_async(self, teacher_id: int) -> Optional[Teacher]:
        result = await self.session.execute(
            select(TeacherDto).where(TeacherDto.self_id == teacher_id))
        dto = result.scalar_one_or_none()
        return TeacherMapper.to_entity(dto) if dto else None

    async def add_async(self, teacher: Teacher) -> Teacher:
        dto = TeacherMapper.to_dto(teacher)
        self.session.add(dto)
        await self.session.commit()
        await self.session.refresh(dto)
        return TeacherMapper.to_entity(dto)

    async def update_async(self, teacher: Teacher) -> Teacher:
        dto = TeacherMapper.to_dto(teacher)
        await self.session.execute(
            update(TeacherDto)
            .where(TeacherDto.self_id == dto.self_id)
            .values(
                name=dto.name,
                subjects=dto.subjects,
                requisites=dto.requisites,
                telegram_tag=dto.telegram_tag
            )
        )
        await self.session.commit()
        return teacher

    async def delete_async(self, teacher_id: int) -> bool:
        result = await self.session.execute(
            delete(TeacherDto).where(TeacherDto.self_id == teacher_id))
        await self.session.commit()
        return result.rowcount > 0
