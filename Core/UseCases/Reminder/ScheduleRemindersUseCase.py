from datetime import datetime, timedelta
from typing import List
from Core.Entities.Lesson import Lesson
from Core.Entities.Reminder import Reminder
from Core.Interfaces.ILessonRepository import ILessonRepository
from Core.Interfaces.IReminderRepository import IReminderRepository
from Core.Interfaces.ITimeSlotRepository import ITimeSlotRepository


class ScheduleRemindersUseCase:
    def __init__(
        self,
        lesson_repo: ILessonRepository,
        time_slot_repo: ITimeSlotRepository,
        reminder_repo: IReminderRepository
    ):
        self._lesson_repo = lesson_repo
        self._time_slot_repo = time_slot_repo
        self._reminder_repo = reminder_repo

    async def execute(self, hours_ahead: int = 24) -> List[Reminder]:
        """
        Создает напоминания для всех уроков, которые начнутся в ближайшие `hours_ahead` часов.
        Напоминания создаются за 24 часа и за 1 час до начала урока.
        """
        lessons = await self._get_upcoming_lessons(hours_ahead)
        reminders = []

        for lesson in lessons:
            # Создаем напоминания за 24 часа и 1 час до урока
            for offset_hours in [24, 1]:
                reminder = await self._create_reminder(lesson, offset_hours)
                if reminder:
                    reminders.append(reminder)

        return reminders

    async def _get_upcoming_lessons(self, hours_ahead: int) -> List[Lesson]:
        """Получает уроки, которые начнутся в ближайшие `hours_ahead` часов."""
        now = datetime.now()
        future_time = now + timedelta(hours=hours_ahead)

        # Получаем временные слоты, попадающие в интервал [now, future_time]
        time_slots = await self._time_slot_repo.get_slots_by_date_range_async(
            start_date=now.date(),
            end_date=future_time.date()
        )

        # Получаем уроки для этих слотов
        time_slot_ids = [slot.self_id for slot in time_slots]
        return await self._lesson_repo.get_lessons_by_time_slots_async(time_slot_ids)

    async def _create_reminder(
            self,
            lesson: Lesson,
            offset_hours: int
    ) -> Reminder:
        """Создает напоминание, если оно еще не существует."""
        time_slot = await self._time_slot_repo.get_by_id_async(lesson.time_slot_id)
        if not time_slot:
            return None  # Слот не найден

        lesson_start = datetime.combine(time_slot.slot_date, time_slot.start_time)
        reminder_time = lesson_start - timedelta(hours=offset_hours)

        # Проверяем, не создано ли уже такое напоминание
        existing = await self._reminder_repo.get_by_lesson_id_and_trigger_time_async(
            lesson_id=lesson.self_id,
            trigger_time=reminder_time
        )
        if existing:
            return None  # Напоминание уже существует

        reminder = Reminder.create(
            self_id=None,
            lesson_id=lesson.self_id,
            student_id=lesson.student_id,
            trigger_time=reminder_time,
            time_before_lesson=timedelta(hours=offset_hours),
            is_sent=False
        )

        await self._reminder_repo.add_async(reminder)
        return reminder
