from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, Field, AnyUrl


class ArtistBase(BaseModel):
    spotify_id: str
    name: str
    type: str = "artist"
    followers: int = 0
    popularity: int = 0
    genres: list[str]
    image_url: AnyUrl | None


class ArtistSchema(ArtistBase):
    class Config:
        orm_mode = True


class ArtistSchemaUpdate(ArtistBase):
    spotify_id: str | None
    name:  str | None
    type:  str | None
    followers:  int | None
    popularity:  int | None
    genres: list[str] | None

    class Config:
        orm_mode = True


class ArtistResponse(ArtistBase):
    id: UUID
    created_at: datetime
    is_api_managed: bool

    class Config:
        orm_mode = True


class ArtistFromExternal(BaseModel):
    spotify_id: str
    name: str
    type: str = "artist"
    followers: int = 0
    popularity: int = 0
    genres: list[str]
    image_url: AnyUrl | None

