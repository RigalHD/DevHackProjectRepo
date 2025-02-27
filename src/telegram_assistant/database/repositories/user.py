from collections.abc import Sequence
from typing import Any

from aiogram.types import User as AiogramUser
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from telegram_assistant.database.models.user import BotAdministrators, TelegramUsers
from telegram_assistant.database.repositories.abstract import Repository


class TelegramUsersRepository(Repository[TelegramUsers]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(type_model=TelegramUsers, session=session)

    async def create(
        self,
        aiogram_user: AiogramUser,
    ) -> None:
        user = TelegramUsers(
            telegram_id=aiogram_user.id,
            first_name=aiogram_user.first_name or "",
            last_name=aiogram_user.last_name or "",
            username=aiogram_user.username or "",
        )
        await self.session.merge(user)
        await self.session.commit()

    async def update(
        self,
        telegram_id: int,
        **kwargs: dict[str, Any],
    ) -> None:
        user = await self.get(telegram_id)
        if user:
            if "telegram_id" in kwargs:
                raise ValueError("telegram_id cannot be changed")
            if "registation_datetime" in kwargs:
                raise ValueError("registation_datetime cannot be changed")
            for key, value in kwargs.items():
                if hasattr(user, key):
                    setattr(user, key, value)
                await self.session.commit()
        else:
            raise ValueError("User not found")


class BotAdministratorsRepository(Repository[BotAdministrators]):
    type_model: type[BotAdministrators]

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(type_model=BotAdministrators, session=session)

    async def create(
        self,
        telegram_id: int,
        permissions_level: int = 1,
    ) -> None:
        user = await TelegramUsersRepository(self.session).get(telegram_id)
        admin = self.type_model(permissions_level=permissions_level)
        admin.telegram_profile = user
        await self.session.merge(admin)
        await self.session.commit()

    async def get_by_permissions_level(self, perms_level: int) -> Sequence[BotAdministrators]:
        """:param perms_level: Уровнень прав пользователя"""
        stmt = select(
            self.type_model,
        ).where(self.type_model.permissions_level >= perms_level)
        result = await self.session.scalars(stmt)
        return result.all()
