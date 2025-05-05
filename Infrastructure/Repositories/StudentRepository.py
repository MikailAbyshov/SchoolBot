from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from typing import List, Optional
from Core.Entities.Student import Student
from Core.Interfaces.IStudentRepository import IStudentRepository
from Infrastructure.Dto.StudentDto import StudentDto
from Infrastructure.Mappers.StudentMapper import StudentMapper

class StudentRepository(IStudentRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all_async(self) -> List[Student]:
        result = await self.session.execute(select(StudentDto))
        return [StudentMapper.to_entity(dto) for dto in result.scalars()]

    async def get_by_id_async(self, student_id: int) -> Optional[Student]:
        result = await self.session.execute(
            select(StudentDto).where(StudentDto.self_id == student_id))
        dto = result.scalar_one_or_none()
        return StudentMapper.to_entity(dto) if dto else None

    async def add_async(self, student: Student) -> Student:
        dto = StudentMapper.to_dto(student)
        self.session.add(dto)
        await self.session.commit()
        await self.session.refresh(dto)
        return StudentMapper.to_entity(dto)

    async def update_async(self, student: Student) -> Student:
        dto = StudentMapper.to_dto(student)
        await self.session.execute(
            update(StudentDto)
            .where(StudentDto.self_id == dto.self_id)
            .values(
                name=dto.name,
                email=dto.email,
                telegram_tag=dto.telegram_tag
            )
        )
        await self.session.commit()
        return student

    async def delete_async(self, student_id: int) -> bool:
        result = await self.session.execute(
            delete(StudentDto).where(StudentDto.self_id == student_id))
        await self.session.commit()
        return result.rowcount > 0

    async def get_by_student_contact_async(self, student_contact: str) -> Optional[Student]:
        """
        Ищет студента по его контактам (полю student_contact).
        """
        stmt = select(StudentDto).where(StudentDto.student_contact == student_contact)
        result = await self.session.execute(stmt)
        dto = result.scalars().first()
        return StudentMapper.to_entity(dto) if dto else None

    async def get_by_parent_contact_async(self, parent_contact: str) -> List[Student]:
        """
        Возвращает список студентов по тегу родителя (parent_contact).
        """
        stmt = select(StudentDto).where(StudentDto.parent_contact == parent_contact)
        result = await self.session.execute(stmt)
        dtos = result.scalars().all()
        return [StudentMapper.to_entity(dto) for dto in dtos]
