from collections.abc import Awaitable, Callable
from typing import Any

from aiogram import BaseMiddleware, Router
from aiogram.dispatcher.flags import get_flag
from aiogram.types import CallbackQuery, Message
from sqlalchemy.ext.asyncio import AsyncSession

from telegram_assistant.database.db import Database
from telegram_assistant.database.models import TelegramUsers

router = Router()


class PermissionsCheckMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, dict[str, Any]], Awaitable[Any]],
        event: Message | CallbackQuery,
        data: dict[str, Any],
    ) -> Any:
        flg = get_flag(data, "needed_perms_level")
        if flg:
            async with AsyncSession(data["engine"]) as session:
                user_repo = Database(session=session).telegram_users
                user: TelegramUsers | None = await user_repo.get(event.from_user.id)
                if not user.admin_profile:
                    return None
                if user.admin_profile.permissions_level < flg:
                    return None

        return await handler(event, data)
