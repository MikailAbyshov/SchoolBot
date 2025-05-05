from Core.Entities.Student import Student
from Application.Respones.Student.ResponseStudentInitial import ResponseStudentInitial
from Application.Respones.Student.ResponseParentInitial import ResponseParentInitial
from Application.Respones.Student.ResponseStudentBriefForParent import ResponseStudentBriefForParent
from typing import List

class StudentMapper:
    @staticmethod
    def from_ent_to_initial_response(ent: Student) -> ResponseStudentInitial:
        return ResponseStudentInitial(
            self_id=ent.self_id,
            name=ent.name,
            tg_teg=ent.student_contact,
            parent_name=ent.parent_name,
            parent_tg_teg=ent.parent_contact,
            timezone=ent.timezone
        )

    @staticmethod
    def from_ent_to_brief_for_parent(ent: Student) -> ResponseStudentBriefForParent:
        return ResponseStudentBriefForParent(
            self_id=ent.self_id,
            name=ent.name,
            tg_teg=ent.student_contact,
            payment_status=ent.payment_status
        )

    @staticmethod
    def from_ents_to_initial_parent(ents: List[Student]) -> ResponseParentInitial:
        studentsbrief = [StudentMapper.from_ent_to_brief_for_parent(ent) for ent in ents]
        return ResponseParentInitial(
            name=ents[0].parent_name,
            tg_teg=ents[0].parent_contact,
            timezone=ents[0].timezone,
            students=studentsbrief
        )