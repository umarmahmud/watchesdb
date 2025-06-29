from pydantic import BaseModel, Field
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

# sqlalchemy models
class Base(DeclarativeBase):
    pass


class UserTable(Base):
    __tablename__ = "users"

    username: Mapped[str] = mapped_column(primary_key=True)
    pwd: Mapped[str]

# pydantic model
class User(BaseModel):
    username: str
    pwd: str

