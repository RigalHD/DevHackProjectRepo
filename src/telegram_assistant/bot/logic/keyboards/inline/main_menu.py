from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from telegram_assistant.bot.logic.callbackdata import MainMenuCBData
from telegram_assistant.bot.logic.callbackdata.main_menu_cb_data import QuestionCBData


def main_menu_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text="Узнать o ЮФУ",
            callback_data=QuestionCBData(
                action="Question",
                question_id="1",
                ).pack(),
        ),
        InlineKeyboardButton(
            text="Кафедры", # Расскажи о кафедрах ЮФУ
            callback_data=MainMenuCBData(action="BackToMainMenu").pack(),
        ),
        InlineKeyboardButton(
            text="Преподаватели", # Расскажи о преподавателе <ФИО> из ЮФУ
            callback_data=MainMenuCBData(action="BackToMainMenu").pack(),
        ),
    )
    builder.row(
        InlineKeyboardButton(
            text="Поступление", # Расскажи о поступлении в ЮФУ
            callback_data=QuestionCBData(
                action="Question",
                question_id="2",
                ).pack(),
        ),
        InlineKeyboardButton(
            text="Расписание", # дадим ссылку
            callback_data=MainMenuCBData(action="BackToMainMenu").pack(),
        ),
        InlineKeyboardButton(
            text="Мероприятия", # Расскажи о последних мероприятих ЮФУ + опционально(, основываясь на постах)
            callback_data=QuestionCBData(
                action="Question",
                question_id="3",
                ).pack(),
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
