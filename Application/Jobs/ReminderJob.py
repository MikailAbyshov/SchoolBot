from Core.Interfaces.ILessonRepository import ILessonRepository
from Core.Interfaces.ITimeSlotRepository import ITimeSlotRepository
from Core.Interfaces.IReminderRepository import IReminderRepository
from Core.UseCases.Reminder.ScheduleRemindersUseCase import ScheduleRemindersUseCase

class ReminderJob:
    def __init__(
        self,
        lesson_repo: ILessonRepository,
        time_slot_repo: ITimeSlotRepository,
        reminder_repo: IReminderRepository
    ):
        self._lesson_repo = lesson_repo
        self._time_slot_repo = time_slot_repo
        self._reminder_repo = reminder_repo
        # подготовим use-case
        self._use_case = ScheduleRemindersUseCase(
            self._lesson_repo,
            self._time_slot_repo,
            self._reminder_repo
        )

    async def run(self) -> list[dict]:
        """
        Создаёт напоминания (за 1 час и за 24 часа, как в UseCase)
        и собирает список уведомлений для отправки.
        """
        # 1. Сгенерировать новые напоминания
        reminders = await self._use_case.execute(hours_ahead=1)
        print(f"[ReminderJob] Создано напоминаний: {len(reminders)}")

        # 2. Превратить их в DTO для планировщика
        notifications = []
        for reminder in reminders:
            notifications.append({
                'reminder_id':   reminder.self_id,
                'student_id':    reminder.student_id,  # это внутренний PK студента
                'lesson_id':     reminder.lesson_id,
                'trigger_time':  reminder.trigger_time
            })
        return notifications
