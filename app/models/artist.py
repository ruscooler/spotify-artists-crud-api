import uuid
from datetime import datetime

from sqlalchemy import Column, String, Integer, ARRAY, DateTime, Boolean, select
from sqlalchemy.dialects import postgresql
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.base import Base
from app.utils import get_logger

logger = get_logger(__name__)


class Artist(Base):
    __tablename__ = "artist"

    id = Column(postgresql.UUID(as_uuid=True), unique=True, default=uuid.uuid4, primary_key=True, index=True)
    spotify_id = Column(String(255), unique=True, nullable=False, index=True)
    name = Column(String, nullable=False)
    type = Column(String)
    followers = Column(Integer)
    popularity = Column(Integer)
    genres = Column(ARRAY(String))
    image_url = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    is_api_managed = Column(Boolean, default=False, nullable=False)

    @classmethod
    async def update_or_create(cls, db_session: AsyncSession, obj: "Artist"):
        result = await db_session.execute(select(cls).where(cls.spotify_id == obj.spotify_id))
        instance = result.scalars().first()

        if instance is None:
            await obj.save(db_session)
        elif not instance.is_api_managed:
            await db_session.merge(obj)
        else:
            logger.info(f"Artist {obj.name} ({obj.id}) has already been changed by the user via the API, "
                        f"modifying is not possible")
