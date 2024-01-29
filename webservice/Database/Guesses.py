from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.exc import List

from .Base import Base


class Guesses(Base):
    __tablename__ = "guesses"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    result: Mapped[int] = mapped_column(
        ForeignKey("gameresults.id", ondelete="CASCADE"),
        autoincrement=False,
    )
    game: Mapped[int] = mapped_column(
        ForeignKey("games.id", ondelete="CASCADE"),
        autoincrement=False,
    )
    guess_num: Mapped[int]
    guess: Mapped[str]
    result1: Mapped[str]
    result2: Mapped[str]
    result3: Mapped[str]
    result4: Mapped[str]
    result5: Mapped[str]

    resultdetails: Mapped["GameResults"] = relationship()
    gamedetails: Mapped["Games"] = relationship()
