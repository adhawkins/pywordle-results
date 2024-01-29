from sqlalchemy import Date
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.exc import List
import datetime

from .Base import Base


class Games(Base):
    __tablename__ = "games"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=False)
    date: Mapped[datetime.date] = mapped_column(Date, server_default=func.now())
    solution: Mapped[str]
