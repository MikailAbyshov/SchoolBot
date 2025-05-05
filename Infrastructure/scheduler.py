from datetime import date, timedelta
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from Infrastructure.Config import async_session_factory
from Infrastructure.Repositories.TimeSlotRepository import TimeSlotRepository
from Core.UseCases.TimeSlot.TimeSlotGenerator import run_slot_generation_use_case


async def weekly_slot_generator_job():
    """
    Функция, вызываемая по расписанию для генерации таймслотов.
    При первом запуске, если слотов нет, генерируются слоты на месяц вперёд (от сегодняшнего дня).
    Если слоты уже есть, добавляются недостающие слоты, чтобы покрыть период до (сегодня + 30 дней).
    """
    async with async_session_factory() as session:
        repository = TimeSlotRepository(session)
        today = date.today()
        forward_boundary = today + timedelta(days=30)  # Дата, до которой нужны слоты
        backward_boundary = today - timedelta(days=14)  # Дата, начиная с которой слоты должны храниться

        min_date = await repository.get_min_slot_date_async()
        max_date = await repository.get_max_slot_date_async()
        forward_boundary = date.today() + timedelta(days=30)

        if max_date == today:
            # Если таблица пуста – генерировать слоты от сегодняшнего дня до (today + 30)
            start_date = max_date
            end_date = forward_boundary
        else:
            if min_date < backward_boundary:
                print(f"Удаление таймслотов до {backward_boundary} (минимальная дата в таблице: {min_date})")
                await repository.delete_slots_before_date_async(backward_boundary)

            # Если есть слоты, и самый поздний слот меньше, чем forward_boundary – генерировать недостающие слоты
            if max_date < forward_boundary:
                start_date = max_date + timedelta(days=1)
                end_date = forward_boundary
            else:
                return
        print(f"Генерация таймслотов с {start_date} до {end_date}")
        await run_slot_generation_use_case(repository, start_date, end_date)


def start_scheduler():
    """Настраиваем и запускаем планировщик фоновых задач."""
    scheduler = AsyncIOScheduler()
    # Планируем задачу по расписанию. Например, каждый понедельник в 00:00:
    scheduler.add_job(weekly_slot_generator_job, 'cron', day_of_week='wed', hour=10, minute=30)
    scheduler.start()
    print("Сервис генерации расписания запущен.")


if __name__ == '__main__':
    import asyncio


    async def main():
        print("⏳ Первый запуск: генерация таймслотов...")
        await weekly_slot_generator_job()  # Однократный вызов при старте

        print("📅 Запуск планировщика...")
        start_scheduler()

        print("✅ Сервис расписания готов к работе.")
        while True:
            await asyncio.sleep(3600)  # Заглушка, чтобы event loop не завершался


    asyncio.run(main())
