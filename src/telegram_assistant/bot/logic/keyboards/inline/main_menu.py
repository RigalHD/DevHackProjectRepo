from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from telegram_assistant.bot.logic.callbackdata import MainMenuCBData


def main_menu_kb(user_admin_profile: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    if user_admin_profile:
        builder.row(
            InlineKeyboardButton(
            text="Админ-панель",
            callback_data=MainMenuCBData(action="AdminPanelView").pack(),
            ),
        )

    return builder.as_markup()


def back_to_main_menu_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
        text="В главное меню",
        callback_data=MainMenuCBData(action="BackToMainMenu").pack(),
        ),
    )

    return builder.as_markup()
