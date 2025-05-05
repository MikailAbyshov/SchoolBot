from Core.Entities.TimeSlot import TimeSlot
from Infrastructure.Dto.TimeSlotDto import TimeSlotDto

class TimeSlotMapper:
    @staticmethod
    def to_entity(dto: TimeSlotDto) -> TimeSlot:
        return TimeSlot.create(
            self_id=dto.self_id,
            slot_date=dto.slot_date,
            start_time=dto.start_time,
            end_time=dto.end_time,
            is_booked=dto.is_booked
        )

    @staticmethod
    def to_dto(entity: TimeSlot) -> TimeSlotDto:
        return TimeSlotDto(
            self_id=entity.self_id,
            slot_date=entity.slot_date,
            start_time=entity.start_time,
            end_time=entity.end_time,
            is_booked=entity.is_booked
        )
