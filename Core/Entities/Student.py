from dataclasses import dataclass
@dataclass
class Student:
    self_id: int
    name: str
    timezone: str
    parent_name: str
    parent_contact: str
    student_contact: str
    payment_status: int
    teacher_id: int

    @classmethod
    def create(
            cls,
            self_id: int,
            name: str,
            timezone: str,
            parent_name: str,
            parent_contact: str,
            student_contact: str,
            payment_status: int,
            teacher_id: int
    ) -> "Student":
        if (self_id is not None) and (self_id < 1):
            raise ValueError("id должен быть >= 1")
        if len(name) > 100:
            raise ValueError("Макс. длина name 100 символов")
        if len(timezone) > 100:
            raise ValueError("Макс. длина timezone 100 символов")
        if len(parent_name) > 100:
            raise ValueError("Макс. длина parent_name 100 символов")
        if len(parent_contact) > 100:
            raise ValueError("Макс. длина parent_contact 100 символов")
        if len(student_contact) > 100:
            raise ValueError("Макс. длина name 100 символов")
        if payment_status < 0:
            raise ValueError("payment_status должен быть положительным")
        if teacher_id < 1:
            raise ValueError("teacher_id должен быть >= 1")
        return cls(self_id, name, timezone, parent_name, parent_contact,
                   student_contact, payment_status, teacher_id)
