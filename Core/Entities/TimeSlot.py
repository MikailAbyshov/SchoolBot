from datetime import time, date
from dataclasses import dataclass

@dataclass
class TimeSlot:
    self_id: int
    slot_date: date          # Дата слота (2023-10-05)
    start_time: time    # Начало (07:00)
    end_time: time      # Конец (07:30)
    is_booked: bool = False  # Занят ли слот

    @classmethod
    def create(
            cls,
            self_id: int,  # Добавляем id в фабричный метод
            slot_date: date,
            start_time: time,
            end_time: time,
            is_booked: bool = False
    ) -> "TimeSlot":
        # Валидация данных
        if start_time >= end_time:
            raise ValueError("Время начала должно быть раньше окончания")
        if (end_time.hour * 60 + end_time.minute) - (start_time.hour * 60 + start_time.minute) != 30:
            raise ValueError("Слот должен длиться 30 минут")
        if (self_id is not None) and (self_id < 1):
            raise ValueError("id должен быть >= 1")
        return cls(self_id, slot_date, start_time, end_time, is_booked)
