from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from telegram_assistant.bot.logic.callbackdata import (
    MainMenuCBData,
)


def admin_panel_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.row(
        InlineKeyboardButton(
            text="В главное меню",
            callback_data=MainMenuCBData(action="BackToMainMenu").pack(),
        ),
    )

    return builder.as_markup()


def back_to_admin_panel_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text="В админ-панель",
            callback_data=MainMenuCBData(action="AdminPanelView").pack(),
        ),
    )

    return builder.as_markup()
