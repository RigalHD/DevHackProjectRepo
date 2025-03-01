from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from telegram_assistant.bot.logic.keyboards.inline import (
    main_menu_kb,
)

router = Router()


@router.message(CommandStart())
async def start(message: Message) -> None:
    message_text = f"<b>Приветствую, {message.from_user.first_name}</b>"

    await message.answer(
        text=message_text,
        reply_markup=main_menu_kb(),
    )
