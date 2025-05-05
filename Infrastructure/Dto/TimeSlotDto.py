from sqlalchemy import Column, Date, Time, Boolean, Integer
from Infrastructure.Config import Base


class TimeSlotDto(Base):
    __tablename__ = "time_slots"

    self_id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    slot_date = Column(Date, nullable=False)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    is_booked = Column(Boolean, default=False)
