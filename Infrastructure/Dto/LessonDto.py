from Infrastructure.Config import Base
from sqlalchemy import Column, String, Integer, ForeignKey

class LessonDto(Base):
    __tablename__ = "lessons"

    self_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    time_slot_id = Column(Integer, ForeignKey("time_slots.self_id"), nullable=False)
    title = Column(String(collation="NOCASE"), nullable=False)
    teacher_id = Column(Integer, ForeignKey("teachers.self_id"), nullable=False)
    student_id = Column(Integer, ForeignKey("students.self_id", ondelete="CASCADE"), nullable=False)


