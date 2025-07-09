from enum import Enum

from pydantic import BaseModel
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from ..db import Base

class MovementType(Enum):
    automatic = "automatic"
    manual = "manual"
    quartz = "quartz"


# sqlalchemy models
class MovementTable(Base):
    __tablename__ = "movements"

    movement: Mapped[str] = mapped_column(primary_key=True)
    movement_type: Mapped[MovementType]
    jewels: Mapped[int]
    power_reserve: Mapped[int]
    manufacturer: Mapped[str] = mapped_column(ForeignKey("manufacturers.manufacturer"))


# pydantic models
class Movement(BaseModel):
    movement: str
    movement_type: MovementType | None = None
    jewels: int | None = None
    power_reserve: int | None = None
    manufacturer: str
    