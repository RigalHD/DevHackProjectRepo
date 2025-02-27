from datetime import datetime

from sqlalchemy import BigInteger, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import BaseModel


class TelegramUsers(BaseModel):
    __tablename__ = "telegram_users"

    telegram_id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        unique=True,
        nullable=False,
    )
    first_name: Mapped[str] = mapped_column(nullable=True)
    last_name: Mapped[str] = mapped_column(nullable=True)
    username: Mapped[str] = mapped_column(nullable=True)
    registration_datetime: Mapped[datetime] = mapped_column(default=datetime.now)
    update_datetime: Mapped[datetime] = mapped_column(nullable=True, onupdate=datetime.now)
    phone_number: Mapped[str] = mapped_column(nullable=True)
    admin_profile: Mapped["BotAdministrators"] = relationship(
        back_populates="telegram_profile",
        uselist=False,
        lazy="selectin",
    )

    def __str__(self) -> str:
        return f"<telegram_id={self.telegram_id}>"

    def __repr__(self) -> str:
        return f"<telegram_id={self.telegram_id}>"


class BotAdministrators(BaseModel):
    __tablename__ = "bot_administrators"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    telegram_profile: Mapped["TelegramUsers"] = relationship(
        back_populates="admin_profile",
        uselist=False,
    )
    telegram_id: Mapped[int] = mapped_column(
        ForeignKey(column="telegram_users.telegram_id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
    )
    permissions_level: Mapped[int] = mapped_column(default=0)

    registation_datetime: Mapped[datetime] = mapped_column(default=datetime.now, nullable=True)
    update_datetime: Mapped[datetime] = mapped_column(nullable=True, onupdate=datetime.now)

    def __str__(self) -> str:
        return f"<telegram_id={self.telegram_id}>"

    def __repr__(self) -> str:
        return f"<telegram_id={self.telegram_id}>"
