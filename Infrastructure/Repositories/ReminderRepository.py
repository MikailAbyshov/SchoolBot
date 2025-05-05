from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete, and_
from datetime import datetime
from typing import List, Optional
from Core.Entities.Reminder import Reminder
from Core.Interfaces.IReminderRepository import IReminderRepository
from Infrastructure.Dto.ReminderDto import ReminderDto
from Infrastructure.Mappers.ReminderMapper import ReminderMapper

class ReminderRepository(IReminderRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all_async(self) -> List[Reminder]:
        result = await self.session.execute(select(ReminderDto))
        return [ReminderMapper.to_entity(dto) for dto in result.scalars()]

    async def add_async(self, reminder: Reminder) -> Reminder:
        dto = ReminderMapper.to_dto(reminder)
        self.session.add(dto)
        await self.session.commit()
        await self.session.refresh(dto)
        return ReminderMapper.to_entity(dto)

    async def update_async(self, reminder: Reminder) -> Reminder:
        dto = ReminderMapper.to_dto(reminder)
        await self.session.execute(
            update(ReminderDto)
            .where(ReminderDto.self_id == dto.self_id)
            .values(
                lesson_id=dto.lesson_id,
                user_id=dto.user_id,
                trigger_time=dto.trigger_time,
                is_sent=dto.is_sent
            )
        )
        await self.session.commit()
        return reminder

    async def delete_async(self, reminder_id: int) -> bool:
        result = await self.session.execute(
            delete(ReminderDto).where(ReminderDto.self_id == reminder_id)
        )
        await self.session.commit()
        return result.rowcount > 0

    async def get_by_id_async(self, reminder_id: int) -> Optional[Reminder]:
        result = await self.session.execute(
            select(ReminderDto).where(ReminderDto.self_id == reminder_id)
        )
        dto = result.scalar_one_or_none()
        return ReminderMapper.to_entity(dto) if dto else None

    async def get_pending_reminders_async(self, target_time: datetime) -> List[Reminder]:
        result = await self.session.execute(
            select(ReminderDto)
            .where(
                and_(
                    ReminderDto.trigger_time <= target_time,
                    ReminderDto.is_sent == False
                )
            )
        )
        return [ReminderMapper.to_entity(dto) for dto in result.scalars()]

    async def get_by_lesson_id_and_trigger_time_async(
        self,
        lesson_id: int,
        trigger_time: datetime
    ) -> Optional[Reminder]:
        result = await self.session.execute(
            select(ReminderDto)
            .where(
                and_(
                    ReminderDto.lesson_id == lesson_id,
                    ReminderDto.trigger_time == trigger_time
                )
            )
        )
        dto = result.scalar_one_or_none()
        return ReminderMapper.to_entity(dto) if dto else None

    async def mark_as_sent_async(self, reminder_id: int) -> None:
        await self.session.execute(
            update(ReminderDto)
            .where(ReminderDto.self_id == reminder_id)
            .values(is_sent=True)
        )
        await self.session.commit()
