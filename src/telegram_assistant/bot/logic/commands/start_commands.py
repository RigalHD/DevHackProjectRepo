from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from telegram_assistant.bot.logic.keyboards.inline import (
    main_menu_kb,
)
from telegram_assistant.database import Database

router = Router()


@router.message(CommandStart(), flags={"needed_perms_level": 1})
async def start(message: Message, db: Database) -> None:
    message_text = \
        f"<b>Приветствую, {message.from_user.first_name}</b>"
    user = await db.telegram_users.get(message.from_user.id)

    await message.answer(
        text=message_text,
        reply_markup=main_menu_kb(user.admin_profile),
    )

