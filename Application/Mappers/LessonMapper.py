from Core.Entities.Lesson import Lesson
from Application.Respones.Lesson.ResponseLessonForSchedule import ResponseLessonForSchedule
from datetime import datetime

class LessonMapper:
    @staticmethod
    def from_ent_to_schedule_response(ent: Lesson, lesson_datetime: datetime, lesson_teacher_name) -> ResponseLessonForSchedule:
        return ResponseLessonForSchedule(
            subject_name=ent.title,
            self_datetime=lesson_datetime,
            teacher_name=lesson_teacher_name
        )