from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from telegram_assistant.bot.logic.callbackdata import MainMenuCBData


def main_menu_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text="Узнать o ЮФУ",
            callback_data=MainMenuCBData(action="BackToMainMenu").pack(),
        ),
        InlineKeyboardButton(
            text="Кафедрах",
            callback_data=MainMenuCBData(action="BackToMainMenu").pack(),
        ),
        InlineKeyboardButton(
            text="Преподаватели",
            callback_data=MainMenuCBData(action="BackToMainMenu").pack(),
        ),
    )
    builder.row(
        InlineKeyboardButton(
            text="Поступление",
            callback_data=MainMenuCBData(action="BackToMainMenu").pack(),
        ),
        InlineKeyboardButton(
            text="Расписание",
            callback_data=MainMenuCBData(action="BackToMainMenu").pack(),
        ),
        InlineKeyboardButton(
            text="Мероприятия",
            callback_data=MainMenuCBData(action="BackToMainMenu").pack(),
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
