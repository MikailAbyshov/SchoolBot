from sqlalchemy import Column, String, Integer
from Infrastructure.Config import Base

class TeacherDto(Base):
    __tablename__ = 'teachers'

    self_id        = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name           = Column(String(collation="NOCASE"), nullable=False)
    # Здесь для дисциплин можно использовать разные подходы:
    # 1. Хранить как текст, сериализовав список в JSON/строку
    # 2. Создать отдельную таблицу и использовать отношения "один-ко-многим"
    # Пока для примера используем строковое поле
    subjects       = Column(String(collation="NOCASE"), nullable=False)  # Например, "математика,физика,химия"
    requisites     = Column(String, nullable=False)
    telegram_tag   = Column(String(collation="NOCASE"), nullable=False)
    discord_tag    = Column(String(collation="NOCASE"), nullable=False)

    # — Новая колонка для хранения Telegram-ID —
    telegram_id    = Column(Integer, nullable=True)
