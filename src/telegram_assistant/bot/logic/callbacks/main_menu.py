from aiogram import F, Router
from aiogram.types import CallbackQuery

from telegram_assistant.bot.logic.callbackdata import MainMenuCBData
from telegram_assistant.bot.logic.keyboards.inline import main_menu_kb

router = Router()


@router.callback_query(MainMenuCBData.filter(F.action == "BackToMainMenu"))
async def back_to_main_menu_handler(query: CallbackQuery) -> None:
    message_text = f"<b>Приветствую, {query.from_user.first_name}</b>\n\n"

    await query.message.edit_text(
        text=message_text,
        reply_markup=main_menu_kb(),
    )


@router.callback_query(MainMenuCBData.filter(F.action == "BackToMainMenu"))
async def back_to_main_menu_handler(query: CallbackQuery) -> None:
    message_text = f"<b>Приветствую, {query.from_user.first_name}</b>\n\n"

    await query.message.edit_text(
        text=message_text,
        reply_markup=main_menu_kb(),
    )
