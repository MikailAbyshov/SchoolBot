from datetime import date

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete, func, insert
from typing import List, Optional
from Core.Entities.TimeSlot import TimeSlot
from Core.Interfaces.ITimeSlotRepository import ITimeSlotRepository
from Infrastructure.Dto.TimeSlotDto import TimeSlotDto
from Infrastructure.Mappers.TimeSlotMapper import TimeSlotMapper

class TimeSlotRepository(ITimeSlotRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all_async(self) -> List[TimeSlot]:
        result = await self.session.execute(select(TimeSlotDto))
        return [TimeSlotMapper.to_entity(dto) for dto in result.scalars()]

    async def get_by_id_async(self, slot_id: int) -> Optional[TimeSlot]:
        result = await self.session.execute(
            select(TimeSlotDto).where(TimeSlotDto.self_id == slot_id))
        dto = result.scalar_one_or_none()
        return TimeSlotMapper.to_entity(dto) if dto else None

    async def add_async(self, time_slot: TimeSlot) -> TimeSlot:
        dto = TimeSlotMapper.to_dto(time_slot)
        self.session.add(dto)
        await self.session.commit()
        await self.session.refresh(dto)
        return TimeSlotMapper.to_entity(dto)

    async def update_async(self, time_slot: TimeSlot) -> TimeSlot:
        dto = TimeSlotMapper.to_dto(time_slot)
        await self.session.execute(
            update(TimeSlotDto)
            .where(TimeSlotDto.self_id == dto.self_id)
            .values(
                slot_date=dto.slot_date,
                start_time=dto.start_time,
                end_time=dto.end_time,
                is_booked=dto.is_booked
            )
        )
        await self.session.commit()
        return time_slot

    async def delete_async(self, slot_id: int) -> bool:
        result = await self.session.execute(
            delete(TimeSlotDto).where(TimeSlotDto.self_id == slot_id))
        await self.session.commit()
        return result.rowcount > 0

    async def get_by_date_async(self, slot_date: date) -> List[TimeSlot]:
        result = await self.session.execute(
            select(TimeSlotDto).where(TimeSlotDto.slot_date == slot_date))
        return [TimeSlotMapper.to_entity(dto) for dto in result.scalars()]

    async def get_slots_by_date_range_async(
            self,
            start_date: date,
            end_date: date
    ) -> List[TimeSlot]:
        result = await self.session.execute(
            select(TimeSlotDto).where(
                    TimeSlotDto.slot_date >= start_date,
                    TimeSlotDto.slot_date <= end_date
            )
        )
        dtos = result.scalars().all()
        return [TimeSlotMapper.to_entity(dto) for dto in dtos]

    async def get_max_slot_date_async(self) -> date:
        result = await self.session.execute(select(func.max(TimeSlotDto.slot_date)))
        max_date = result.scalar()
        return max_date if max_date is not None else date.today()

    async def add_time_slots_async(self, slots: List[TimeSlot]) -> None:
        """
        Асинхронная bulk вставка слотов в базу данных.
        """
        values = [
            {
                "slot_date": slot.slot_date,
                "start_time": slot.start_time,
                "end_time": slot.end_time,
                "is_booked": slot.is_booked
            }
            for slot in slots
        ]

        stmt = insert(TimeSlotDto).values(values)
        await self.session.execute(stmt)
        await self.session.commit()

    async def get_min_slot_date_async(self) -> date:
        result = await self.session.execute(select(func.min(TimeSlotDto.slot_date)))
        min_date = result.scalar()
        return min_date if min_date is not None else date.today()

    async def delete_slots_before_date_async(self, cutoff_date: date) -> None:
        time_slots = delete(TimeSlotDto).where(TimeSlotDto.slot_date < cutoff_date)
        await  self.session.execute(time_slots)
        await self.session.commit()

    async def get_time_slots_by_ids_async(self, ids: List[int]) -> List[TimeSlot]:
        """
        Возвращает список тайм-слотов, у которых self_id входит в переданный список ids.
        """
        if not ids:
            return []

        stmt = select(TimeSlotDto).where(TimeSlotDto.self_id.in_(ids))
        result = await self.session.execute(stmt)
        dtos = result.scalars().all()
        return [TimeSlotMapper.to_entity(dto) for dto in dtos]


