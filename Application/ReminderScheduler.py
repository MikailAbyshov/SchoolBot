from apscheduler.schedulers.asyncio import AsyncIOScheduler
from sqlalchemy import select

from Infrastructure.Config import async_session_factory
from Infrastructure.Repositories.LessonRepository import LessonRepository
from Infrastructure.Repositories.TimeSlotRepository import TimeSlotRepository
from Infrastructure.Repositories.ReminderRepository import ReminderRepository
from Application.Jobs.ReminderJob import ReminderJob
from Infrastructure.Dto.StudentDto import StudentDto

async def reminder_job_runner(bot):
    """
    Запускается по расписанию, достаёт уведомления и шлёт их через Telegram-бота.
    """
    async with async_session_factory() as session:
        # подготовить репозитории
        lesson_repo  = LessonRepository(session)
        time_repo    = TimeSlotRepository(session)
        reminder_repo= ReminderRepository(session)

        # собрать список сообщений
        job = ReminderJob(lesson_repo, time_repo, reminder_repo)
        notifications = await job.run()

        for note in notifications:
            reminder_id    = note['reminder_id']
            internal_sid   = note['student_id']
            lesson_id      = note['lesson_id']
            trigger_time   = note['trigger_time']

            # 1) Берём из БД Telegram-ID студента
            result = await session.execute(
                select(StudentDto).where(StudentDto.self_id == internal_sid)
            )
            student = result.scalar_one_or_none()
            if not student or not student.student_telegram_id:
                print(f"[ReminderScheduler] Пропуск, нет telegram_id для студента {internal_sid}")
                continue

            chat_id = student.student_telegram_id
            text = f"Напоминание: Урок {lesson_id} начнётся в {trigger_time.strftime('%H:%M')}."

            # 2) Отправка
            try:
                await bot.send_message(chat_id, text)
                print(f"[ReminderScheduler] Отправлено студенту {chat_id} (БД-id {internal_sid}) урок {lesson_id}")
            except Exception as e:
                print(f"[ReminderScheduler] Ошибка при отправке студенту {chat_id}: {e}")
                continue

            # 3) Помечаем как отправленное
            await reminder_repo.mark_as_sent_async(reminder_id)

def start_reminder_scheduler(bot):
    """
    Инициализирует APScheduler (проверка каждую минуту).
    """
    scheduler = AsyncIOScheduler()
    scheduler.add_job(reminder_job_runner, 'interval', minutes=1, args=[bot])
    scheduler.start()
    print("[Scheduler] Сервис уведомлений запущен (интервал = 1 минута).")
