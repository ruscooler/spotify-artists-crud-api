from typing import Optional

from sqlalchemy import Column, String, Integer, DateTime, Boolean, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.base import Base


class BackgroundTask(Base):
    __tablename__ = "background_task"
    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    task_name = Column(String, primary_key=True, index=True)
    is_success = Column(Boolean, nullable=True)
    data = Column(String)
    last_finished_time = Column(DateTime, nullable=False)

    @classmethod
    async def get_by_name(cls, db_session: AsyncSession, name: str) -> Optional["BackgroundTask"]:
        stmt = select(cls).where(cls.task_name == name)
        result = await db_session.execute(stmt)
        return result.scalars().first()
