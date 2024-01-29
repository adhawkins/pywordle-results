from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.schema import UniqueConstraint

from .Base import Base


class GameResults(Base):
    __tablename__ = "gameresults"
    __table_args__ = (UniqueConstraint("user", "game"),)

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        autoincrement=False,
    )
    game: Mapped[int] = mapped_column(
        ForeignKey("games.id", ondelete="CASCADE"),
        autoincrement=False,
    )
    guesses: Mapped[int]
    success: Mapped[int]
    userdetails: Mapped["Users"] = relationship()
    gamedetails: Mapped["Games"] = relationship()
