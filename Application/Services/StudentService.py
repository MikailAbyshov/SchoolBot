from Core.Interfaces.IStudentRepository import IStudentRepository
from Application.Mappers.StudentMapper import StudentMapper
from Application.Respones.Student.ResponseStudentInitial import ResponseStudentInitial
from Application.Respones.Student.ResponseParentInitial import ResponseParentInitial
from typing import Optional

class StudentService:
    def __init__(self,
                 student_repo: IStudentRepository):
        self._student_repo = student_repo

    async def initial_search_student_by_teg(self, teg: str) -> Optional[ResponseStudentInitial]:
        student = await self._student_repo.get_by_student_contact_async(teg)
        if student is None:
            return None
        response = StudentMapper.from_ent_to_initial_response(student)
        return response

    async def initial_search_parent_by_teg(self, teg: str) -> Optional[ResponseParentInitial]:
        students = await self._student_repo.get_by_parent_contact_async(teg)
        if not students:
            return None
        response = StudentMapper.from_ents_to_initial_parent(students)
        return response
