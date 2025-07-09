from pydantic import BaseModel, Field
from sqlalchemy.orm import Mapped, mapped_column

from ..db import Base

# sqlalchemy models
class UserTable(Base):
    __tablename__ = "users"

    username: Mapped[str] = mapped_column(primary_key=True)
    password: Mapped[str]
    is_admin: Mapped[bool]


# pydantic models
class UserCreate(BaseModel):
    username: str
    password: str

    class Config:
        extra = "forbid"


class User(UserCreate):
    is_admin: bool


class Token(BaseModel):
    access_token: str
    token_type: str