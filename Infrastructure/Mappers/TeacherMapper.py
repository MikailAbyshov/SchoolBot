from Core.Entities.Teacher import Teacher
from Infrastructure.Dto.TeacherDto import TeacherDto

class TeacherMapper:
    @staticmethod
    def to_entity(dto: TeacherDto) -> Teacher:
        return Teacher.create(
            self_id=dto.self_id,
            name=dto.name,
            subjects=dto.subjects,
            requisites=dto.requisites,
            telegram_tag=dto.telegram_tag,
            discord_tag=dto.discord_tag,
        )

    @staticmethod
    def to_dto(ent: Teacher) -> TeacherDto:
        return TeacherDto(
            self_id=ent.self_id,
            name=ent.name,
            subjects=ent.subjects,
            requisites=ent.requisites,
            telegram_tag=ent.telegram_tag,
            discord_tag=ent.discord_tag,
        )