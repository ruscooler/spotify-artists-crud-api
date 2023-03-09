from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.artist import Artist
from app.schemas.artist import ArtistSchema, ArtistSchemaUpdate, ArtistResponse
from app.utils import get_logger

router = APIRouter(prefix="/v1/artists")

logger = get_logger(__name__)


@router.get("/all", response_model=list[ArtistResponse])
async def get_all_artist(db_session: AsyncSession = Depends(get_db)):
    artists = await Artist.get_all(db_session)
    return artists


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=ArtistResponse)
async def create_artist(
    payload: ArtistSchema, db_session: AsyncSession = Depends(get_db),
):
    artist = Artist(**payload.dict(), is_api_managed=True)
    await artist.save(db_session)
    return artist


@router.get("/{artist_id}", response_model=ArtistResponse)
async def read_artist(
    artist_id: str,
    db_session: AsyncSession = Depends(get_db),
):
    artists = await Artist.get_or_404(db_session, "id", artist_id)
    return artists


@router.patch("/{artist_id}", response_model=ArtistResponse)
async def update_artist(
    artist_id: str,
    payload: ArtistSchemaUpdate,
    db_session: AsyncSession = Depends(get_db),
):
    artist = await Artist.get_or_404(db_session, "id", artist_id)
    await artist.update(db_session, **payload.dict(exclude_unset=True))
    return artist


@router.delete("/{artist_id}")
async def delete_artist(
    artist_id: str,
    db_session: AsyncSession = Depends(get_db),
):
    artist = await Artist.get_or_404(db_session, "id", artist_id)
    return await artist.delete(db_session)

