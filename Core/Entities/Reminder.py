from dataclasses import dataclass
from datetime import datetime, timedelta

@dataclass
class Reminder:
    self_id: int
    lesson_id: int          # Ссылка на урок
    student_id: int            # ID пользователя (студент/преподаватель)
    trigger_time: datetime  # Когда отправить напоминание
    time_before_lesson: timedelta  # Время которое осталось до урока (больше нужно для более легкой отправки уведомлений)
    is_sent: bool = False   # Статус отправки

    @classmethod
    def create(cls,
               self_id: int,
               lesson_id: int,
               student_id: int,
               trigger_time: datetime,
               time_before_lesson: timedelta,
               is_sent: bool = False
               ) -> "Reminder":
        if (self_id is not None) and (self_id < 1):
            raise ValueError("id должен быть >= 1")
        if lesson_id < 1:
            raise ValueError("lesson_id должен быть >= 1")
        if student_id < 1:
            raise ValueError("student_id должен быть >= 1")

        return cls(self_id, lesson_id,
                   student_id, trigger_time, time_before_lesson, is_sent)
