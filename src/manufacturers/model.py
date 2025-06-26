from pydantic import BaseModel, Field
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

# sqlalchemy models
class Base(DeclarativeBase):
    pass


class ManufacturerTable(Base):
    __tablename__ = "manufacturers"

    manufacturer: Mapped[str] = mapped_column(primary_key=True)
    origin: Mapped[str]
    established: Mapped[int]
    luxury: Mapped[bool]


# pydantic model
class Manufacturer(BaseModel):
    manufacturer: str
    origin: str | None = None
    established: int | None = Field(gt=1000, lt=9999, default=None) 
    luxury: bool | None = None

