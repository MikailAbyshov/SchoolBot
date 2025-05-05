from Infrastructure.Config import Base
from Infrastructure.DBtypes import MinuteInterval
from sqlalchemy import Column, Integer, Boolean, DateTime, ForeignKey


class ReminderDto(Base):
    __tablename__ = "reminders"

    self_id = Column(Integer, primary_key=True, autoincrement=True)
    lesson_id = Column(Integer, ForeignKey("lessons.self_id", ondelete="CASCADE"), nullable=False)
    student_id = Column(Integer, ForeignKey("students.self_id", ondelete="CASCADE"), nullable=False)
    trigger_time = Column(DateTime, nullable=False, index=True)
    time_before_lesson = Column(MinuteInterval, nullable=False, index=True)
    is_sent = Column(Boolean, nullable=False, index=True)
