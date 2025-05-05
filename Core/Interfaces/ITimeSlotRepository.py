from abc import ABC, abstractmethod
from Core.Entities.TimeSlot import TimeSlot
from typing import List, Optional
from datetime import date

class ITimeSlotRepository(ABC):
    @abstractmethod
    async def get_all_async(self) -> List[TimeSlot]:
        pass

    @abstractmethod
    async def get_by_id_async(self, slot_id: int) -> Optional[TimeSlot]:
        pass

    @abstractmethod
    async def add_async(self, time_slot: TimeSlot) -> TimeSlot:
        pass

    @abstractmethod
    async def update_async(self, time_slot: TimeSlot) -> TimeSlot:
        pass

    @abstractmethod
    async def delete_async(self, slot_id: int) -> bool:
        pass

    @abstractmethod
    async def get_by_date_async(self, target_date: date) -> List[TimeSlot]:
        pass

    @abstractmethod
    async def get_slots_by_date_range_async(
            self,
            start_date: date,
            end_date: date
    ) -> List[TimeSlot]:
        """Возвращает слоты в диапазоне дат [start_date, end_date]."""
        pass

    @abstractmethod
    async def add_time_slots_async(self, slots: List[TimeSlot]) -> None:
        """Сохраняет список time‑слотов."""
        pass

    @abstractmethod
    async def get_max_slot_date_async(self) -> date:
        """Возвращает самую позднюю дату, на которую сгенерированы слоты."""
        pass

    @abstractmethod
    async def get_min_slot_date_async(self) -> date:
        """Возвращает ранюю (старую) позднюю дату, на которую сгенерированы слоты."""
        pass

    @abstractmethod
    async def delete_slots_before_date_async(self, cutoff_date: date) -> None:
        """Удаляет слота, дата который ранее чем cutoff_date."""
        pass

    @abstractmethod
    async def get_time_slots_by_ids_async(self, ids: List[int]) -> List[TimeSlot]:
        pass
