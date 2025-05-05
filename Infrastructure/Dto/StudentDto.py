from sqlalchemy import Column, Integer, String, ForeignKey
from Infrastructure.Config import Base

class StudentDto(Base):
    __tablename__ = 'students'

    self_id               = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name                  = Column(String(collation="NOCASE"), nullable=False)
    timezone              = Column(String, nullable=False)
    parent_name           = Column(String(collation="NOCASE"), nullable=False)
    parent_contact        = Column(String(collation="NOCASE"), nullable=False)
    student_contact       = Column(String(collation="NOCASE"), nullable=False)
    payment_status        = Column(Integer, nullable=False)
    teacher_id            = Column(Integer, ForeignKey("teachers.self_id"), nullable=False)

    student_telegram_id   = Column(Integer, nullable=True)
    parent_telegram_id    = Column(Integer, nullable=True)
