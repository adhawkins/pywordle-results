from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.schema import UniqueConstraint

from .Base import Base


class TelegramGroups(Base):
    __tablename__ = "telegramgroups"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    group: Mapped[int] = mapped_column(unique=True)
    title: Mapped[str]
