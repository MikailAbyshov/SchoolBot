from Core.Entities.Lesson import Lesson
from Infrastructure.Dto.LessonDto import LessonDto

class LessonMapper:
    @staticmethod
    def to_entity(dto: LessonDto) -> Lesson:
        return Lesson.create(
            self_id=dto.self_id,
            time_slot_id=dto.time_slot_id,
            title=dto.title,
            teacher_id=dto.teacher_id,
            student_id=dto.student_id
        )

    @staticmethod
    def to_dto(ent: Lesson) -> LessonDto:
        return LessonDto(
            self_id=ent.self_id,
            time_slot_id=ent.time_slot_id,
            title=ent.title,
            teacher_id=ent.teacher_id,
            student_id=ent.student_id
        )