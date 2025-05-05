import logging
import asyncio
import sqlite3
import os

from dotenv import load_dotenv

from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from datetime import datetime, timedelta

from Application.Services.StudentService import StudentService
from Application.Services.LessonService import LessonService
from Application.Respones.Student import ResponseStudentInitial, ResponseParentInitial
from Application.ReminderScheduler import start_reminder_scheduler

from Infrastructure.Config import async_session_factory
from Infrastructure.Repositories.StudentRepository import StudentRepository
from Infrastructure.Repositories.LessonRepository import LessonRepository
from Infrastructure.Repositories.TimeSlotRepository import TimeSlotRepository
from Infrastructure.Repositories.TeacherRepository import TeacherRepository

load_dotenv()

BASE_DIR = os.path.dirname(__file__)
DB_PATH  = os.path.join(BASE_DIR, 'online_school.db')

API_TOKEN = os.getenv("BOT_TOKEN")

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher()
user_ids = {}

MONTHS_RU = {
    "January": "января",
    "February": "февраля",
    "March": "марта",
    "April": "апреля",
    "May": "мая",
    "June": "июня",
    "July": "июля",
    "August": "августа",
    "September": "сентября",
    "October": "октября",
    "November": "ноября",
    "December": "декабря",
}


async def create_services():
    session = async_session_factory()

    student_repo = StudentRepository(session)
    lesson_repo = LessonRepository(session)
    time_slot_repo = TimeSlotRepository(session)
    teacher_repo = TeacherRepository(session)

    student_service = StudentService(student_repo)
    lesson_service = LessonService(lesson_repo, time_slot_repo, teacher_repo)

    return student_service, lesson_service


def create_schedule_reset_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="Расписание")], [KeyboardButton(text="Информация")]],
        resize_keyboard=True
    )


@dp.message(Command("start"))
async def start_cmd(message: types.Message):
    username = message.from_user.username
    tg_id    = message.from_user.id

    user_ids[username] = tg_id

    logging.info(f"[START] Получен запрос от пользователя: {username} (ID={tg_id})")

    conn = sqlite3.connect(DB_PATH)
    cur  = conn.cursor()


    cur.execute(
        """
        UPDATE students
           SET student_telegram_id = ?
         WHERE student_contact = ?
        """,
        (tg_id, username)
    )

    cur.execute(
        """
        UPDATE students
           SET parent_telegram_id = ?
         WHERE parent_contact = ?
        """,
        (tg_id, username)
    )
    cur.execute(
        "UPDATE teachers SET telegram_id = ? WHERE telegram_tag = ?",
        (tg_id, username)
    )

    conn.commit()
    conn.close()

    student_service, _ = await create_services()
    student: ResponseStudentInitial = await student_service.initial_search_student_by_teg(username)
    parent:  ResponseParentInitial  = await student_service.initial_search_parent_by_teg(username)

    logging.info(f"[START] Найден студент: {student}")
    logging.info(f"[START] Найден родитель: {parent}")

    if student:
        text = (
            f"Информация об ученике:\n"
            f"Имя ученика: {student.name}\n"
            f"Контакт ученика: {student.tg_teg}\n"
            f"Имя родителя: {student.parent_name}\n"
            f"Контакт родителя: {student.parent_tg_teg}"
        )
        await message.answer(text, reply_markup=create_schedule_reset_keyboard())

    elif parent:
        text = (
            f"Информация о родителе:\n"
            f"Имя родителя: {parent.name}\n"
            f"Контакт родителя: {parent.tg_teg}\n"
            f"Дети:\n"
        )
        for child in parent.students:
            payment_status = "Оплачено" if child.payment_status else "Не оплачено"
            text += (
                f"- Имя ребенка: {child.name}\n"
                f"  Контакт ребенка: {child.tg_teg}\n"
                f"  Статус оплаты: {payment_status}\n"
            )
        await message.answer(text, reply_markup=create_schedule_reset_keyboard())

    else:
        await message.answer(
            "Ваш контакт не найден в базе данных. "
            "Пожалуйста, свяжитесь с администратором."
        )


@dp.message(lambda msg: msg.text == "Расписание")
async def handle_schedule(message: types.Message):
    username = message.from_user.username
    logging.info(f"[SCHEDULE] Запрос расписания от: {username}")
    user_ids[username] = message.from_user.id

    student_service, lesson_service = await create_services()
    student: ResponseStudentInitial = await student_service.initial_search_student_by_teg(username)
    parent: ResponseParentInitial = await student_service.initial_search_parent_by_teg(username)

    logging.info(f"[SCHEDULE] Найден студент: {student}")
    logging.info(f"[SCHEDULE] Найден родитель: {parent}")

    if student:
        lessons = await lesson_service.get_schedule_by_student_id(student.self_id)
        logging.info(f"[SCHEDULE] Уроки для студента {student.name}: {lessons}")

        if lessons:
            response = "Ваше расписание:\n"
            for lesson in lessons:
                date_obj = lesson.self_datetime.date()
                time_obj = lesson.self_datetime.time()
                month_ru = MONTHS_RU[date_obj.strftime("%B")]
                formatted_date = date_obj.strftime(f"%d {month_ru}")
                start = time_obj.strftime("%H:%M")
                end_time = (datetime.combine(date_obj, time_obj) + timedelta(minutes=30)).time()
                end = end_time.strftime("%H:%M")
                response += f"📚 {lesson.subject_name} — {formatted_date} с {start} до {end} (Преподаватель: {lesson.teacher_name})\n"
        else:
            response = "У вас пока нет расписания."
        await message.answer(response)

    elif parent:
        response = "Расписание ваших детей:\n"
        for child in parent.students:
            lessons = await lesson_service.get_schedule_by_student_id(child.self_id)

            if lessons:
                response += f"\n📌 {child.name}:\n"
                for lesson in lessons:
                    date_obj = lesson.self_datetime.date()
                    time_obj = lesson.self_datetime.time()
                    month_ru = MONTHS_RU[date_obj.strftime("%B")]
                    formatted_date = date_obj.strftime(f"%d {month_ru}")
                    start = time_obj.strftime("%H:%M")
                    end_time = (datetime.combine(date_obj, time_obj) + timedelta(minutes=30)).time()
                    end = end_time.strftime("%H:%M")
                    response += f"📚 {lesson.subject_name} — {formatted_date} с {start} до {end} (Преподаватель: {lesson.teacher_name})\n"
            else:
                response += f"\n📌 {child.name}:\nНет запланированных занятий.\n"

        await message.answer(response)

    else:
        await message.answer("Ваш контакт не найден в базе данных.")


@dp.message(Command("reset"))
async def reset_cmd(message: types.Message):
    await message.answer("Вы находитесь на главной странице. Введите команду /start.", reply_markup=ReplyKeyboardRemove())


async def main():
    start_reminder_scheduler(bot)
    dp.message.register(start_cmd)
    dp.message.register(handle_schedule)
    dp.message.register(reset_cmd)
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("Бот остановлен.")
