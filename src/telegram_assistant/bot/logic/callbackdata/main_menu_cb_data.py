from aiogram.filters.callback_data import CallbackData


class MainMenuCBData(CallbackData, prefix="main_menu"):
    action: str


class QuestionCBData(CallbackData, prefix="question"):
    action: str
    question: str
     