from collections.abc import Awaitable, Callable
from typing import Any

from aiogram import BaseMiddleware, Router
from aiogram.types import CallbackQuery, Message
from sqlalchemy.ext.asyncio import AsyncSession

from telegram_assistant.database.db import Database
from telegram_assistant.database.models import TelegramUsers

router = Router()


class RegistrationCheckMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, dict[str, Any]], Awaitable[Any]],
        event: Message | CallbackQuery,
        data: dict[str, Any],
    ) -> Any:
        async with AsyncSession(data["engine"]) as session:
            user_repo = Database(session=session).telegram_users
            user: TelegramUsers | None = await user_repo.get(event.from_user.id)
            if user is not None:
                new_user_data = {}
                if user.first_name != event.from_user.first_name:
                    new_user_data["first_name"] = event.from_user.first_name or ""
                if user.last_name != event.from_user.last_name:
                    new_user_data["last_name"] = event.from_user.last_name or ""
                if user.username != event.from_user.username:
                    new_user_data["username"] = event.from_user.username or ""
                if new_user_data.keys():
                    await user_repo.update(
                        event.from_user.id,
                        **new_user_data,
                    )
            else:
                await user_repo.create(event.from_user)
                await Database(session=session).bot_administrators.create(event.from_user.id, 100)  #!!!! УБРАТЬ!

        return await handler(event, data)
