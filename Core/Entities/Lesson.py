
from dataclasses import dataclass

@dataclass
class Lesson:
    self_id: int
    time_slot_id: int  # Привязка к временному интервалу
    title: str
    teacher_id: int
    student_id: int

    @classmethod
    def create(
            cls,
            self_id: int,
            time_slot_id: int,
            title: str,
            teacher_id: int,
            student_id: int
    ) -> "Lesson":
        if (self_id is not None) and (self_id < 1):
            raise ValueError("id должен быть >= 1")
        if time_slot_id < 1:
            raise ValueError("time_slot_id должен быть >= 1")
        if teacher_id < 1:
            raise ValueError("teacher_id должен быть >= 1")
        if student_id < 1:
            raise ValueError("student_id должен быть >= 1")
        if len(title) > 100:
            raise ValueError("Макс. длина title 100 символов")
        return cls(self_id, time_slot_id, title,
                   teacher_id, student_id)

