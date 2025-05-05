from Core.Entities.Student import Student
from Infrastructure.Dto.StudentDto import StudentDto

class StudentMapper:
    @staticmethod
    def to_entity(dto: StudentDto) -> Student:
        return Student.create(
            self_id=dto.self_id,
            name=dto.name,
            timezone=dto.timezone,
            parent_name=dto.parent_name,
            parent_contact=dto.parent_contact,
            student_contact=dto.student_contact,
            payment_status=dto.payment_status,
            teacher_id=dto.teacher_id
        )

    @staticmethod
    def to_dto(ent: Student) -> StudentDto:
        return StudentDto(
            self_id=ent.self_id,
            name=ent.name,
            timezone=ent.timezone,
            parent_name=ent.parent_name,
            parent_contact=ent.parent_contact,
            student_contact=ent.student_contact,
            payment_status=ent.payment_status,
            teacher_id=ent.teacher_id
        )
