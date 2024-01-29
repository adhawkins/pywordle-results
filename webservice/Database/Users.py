from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.exc import List

from .Base import Base


class Users(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(unique=True)
    fullname: Mapped[str]
