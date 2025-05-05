from Core.Interfaces.ILessonRepository import ILessonRepository
from Application.Respones.Lesson.ResponseLessonForSchedule import ResponseLessonForSchedule
from Core.Interfaces.ITimeSlotRepository import ITimeSlotRepository
from Application.Mappers.LessonMapper import LessonMapper
from Core.Interfaces.ITeacherRepository import ITeacherRepository
from datetime import datetime
from typing import List

class LessonService:
    def __init__(self,
                 lesson_repo: ILessonRepository,
                 time_slot_repo: ITimeSlotRepository,
                 teacher_repo: ITeacherRepository):
        self._lesson_repo = lesson_repo
        self._time_slot_repo = time_slot_repo
        self._teacher_repo = teacher_repo

    async def get_schedule_by_student_id(self, student_id: int) -> List[ResponseLessonForSchedule]:
        """
                Возвращает список занятий для данного студента,
                каждый элемент — ResponseLessonForSchedule.
                """
        # 1) Получаем все уроки студента
        lessons = await self._lesson_repo.get_lessons_by_student_id_async(student_id)
        if not lessons:
            return []

        # 2) Забираем все связанные тайм-слоты и делаем из них словарь
        slot_ids = [lesson.time_slot_id for lesson in lessons]
        slots = await self._time_slot_repo.get_time_slots_by_ids_async(slot_ids)
        slot_map = {slot.self_id: slot for slot in slots}

        response: List[ResponseLessonForSchedule] = []

        for lesson in lessons:
            slot = slot_map.get(lesson.time_slot_id)
            if slot is None:
                return []

            # 3) Берём имя преподавателя (или пустую строку, если не нашли)
            teacher = await self._teacher_repo.get_by_id_async(lesson.teacher_id)
            teacher_name = teacher.name if teacher else ""

            # 4) Собираем DTO, передавая lesson + время + имя
            scheduled_at = datetime.combine(slot.slot_date, slot.start_time)
            resp = LessonMapper.from_ent_to_schedule_response(
                lesson, scheduled_at, teacher_name
            )
            response.append(resp)

        # 5) Сортируем по времени занятия
        response.sort(key=lambda x: x.self_datetime)

        return response

