from datetime import datetime, date, time, timedelta
from typing import List
from Core.Entities.TimeSlot import TimeSlot
from Core.Interfaces.ITimeSlotRepository import ITimeSlotRepository  # Абстракция репозитория

def generate_slots_for_period(start_date: date, end_date: date) -> List[TimeSlot]:
    """
    Генерирует список TimeSlot для каждого дня с start_date до end_date включительно.
    В каждом дне слоты с 07:00 до 22:00 с шагом 30 минут.
    """
    generated_slots = []
    current_date = start_date
    while current_date <= end_date:
        # Определяем время начала для данного дня – 7:00
        current_time = time(7, 0)
        # Последний слот должен начинаться в 21:30 (так как 21:30-22:00)
        while current_time < time(22, 0):
            # Рассчитываем время окончания – прибавляем 30 минут.
            # Для простоты используем timedelta, переводя current_date и current_time в datetime.
            dt_start = datetime.combine(current_date, current_time)
            dt_end = dt_start + timedelta(minutes=30)
            slot = TimeSlot.create(
                self_id=None,  # id будет задан БД
                slot_date=current_date,
                start_time=current_time,
                end_time=dt_end.time(),
                is_booked=False
            )
            generated_slots.append(slot)
            # Переходим к следующему интервалу
            current_time = dt_end.time()
        current_date += timedelta(days=1)
    return generated_slots

async def run_slot_generation_use_case(time_slot_repo: ITimeSlotRepository, start_date: date, end_date: date):
    """
    Генерирует слоты и сохраняет их через репозиторий.
    """
    slots = generate_slots_for_period(start_date, end_date)
    await time_slot_repo.add_time_slots_async(slots)  # Метод репозитория для сохранения списка слотов