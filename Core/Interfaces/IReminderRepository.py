from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Optional
from Core.Entities.Reminder import Reminder

class IReminderRepository(ABC):
    @abstractmethod
    async def get_all_async(self) -> List[Reminder]:
        pass

    @abstractmethod
    async def add_async(self, reminder: Reminder) -> Reminder:
        pass

    @abstractmethod
    async def update_async(self, reminder: Reminder) -> Reminder:
        pass

    @abstractmethod
    async def delete_async(self, reminder_id: int) -> bool:
        pass

    @abstractmethod
    async def get_by_id_async(self, reminder_id: int) -> Optional[Reminder]:
        pass

    @abstractmethod
    async def get_pending_reminders_async(self, target_time: datetime) -> List[Reminder]:
        """Возвращает напоминания, которые нужно отправить (trigger_time <= target_time и is_sent=False)."""
        pass

    @abstractmethod
    async def get_by_lesson_id_and_trigger_time_async(
        self,
        lesson_id: int,
        trigger_time: datetime
    ) -> Optional[Reminder]:
        """Проверяет существование напоминания для урока и времени."""
        pass

    @abstractmethod
    async def mark_as_sent_async(self, reminder_id: int) -> None:
        """Помечает напоминание как отправленное."""
        pass
