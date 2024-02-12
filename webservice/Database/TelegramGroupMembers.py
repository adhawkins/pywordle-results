from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.schema import UniqueConstraint

from .Base import Base


class TelegramGroupMembers(Base):
    __tablename__ = "telegramgroupmembers"
    __table_args__ = (UniqueConstraint("user", "group"),)

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        autoincrement=False,
    )
    group: Mapped[int] = mapped_column(
        ForeignKey("telegramgroups.id", ondelete="CASCADE"),
        autoincrement=False,
    )
    userdetails: Mapped["Users"] = relationship()
    telegramgroupdetails: Mapped["TelegramGroups"] = relationship()
