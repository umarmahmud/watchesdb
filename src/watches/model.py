from pydantic import BaseModel
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from typing import List, Optional

from ..db import Base

# sqlalchemy models
class WatchTable(Base):
    __tablename__ = "watches"

    watch_id: Mapped[int] = mapped_column(primary_key=True)
    manufacturer: Mapped[str] = mapped_column(ForeignKey("manufacturers.manufacturer"))
    model: Mapped[str]
    movement: Mapped[str] = mapped_column(ForeignKey("movements.movement"))
    case_material: Mapped[str]
    case_diameter: Mapped[int]
    dial: Mapped[str]
    crystal: Mapped[str]
    bracelet: Mapped[str]
    strap: Mapped[str]
    trending_price: Mapped[int]
    image_path: Mapped[str]


class FavoriteWatchTable(Base):
    __tablename__ = 'favorites'

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(ForeignKey("users.username"))
    watch_id: Mapped[int] = mapped_column(ForeignKey("watches.watch_id"))


# pydantic models
class WatchCreate(BaseModel):
    manufacturer: str
    model: str
    movement: str | None = None
    case_material: str | None = None
    case_diameter: int | None = None
    dial: str | None = None
    crystal: str | None = None
    bracelet: str | None = None
    strap: str | None = None
    trending_price: int | None = None
    image_path: str | None = None


class Watch(WatchCreate):
    watch_id: int


class FavoriteWatch(BaseModel):
    watch_id: int


class FavoriteWatchGet(BaseModel):
    manufacturer: str
    model: str


class FilterWatchQueryParams(BaseModel):
    manufacturer: Optional[List[str]] = None
    case_material: Optional[List[str]] = None
    case_diameter: Optional[List[int]] = None
    crystal: Optional[List[str]] = None

    class Config:
        extra = "forbid"