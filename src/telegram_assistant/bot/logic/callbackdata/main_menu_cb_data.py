from aiogram.filters.callback_data import CallbackData


class MainMenuCBData(CallbackData, prefix="main_menu"):
    action: str


class QuestionCBData(CallbackData, prefix="question"):
    action: str
    question_id: str


class ParseCBData(CallbackData, prefix="parse"):
    action: str


class DynamicQuestionCBData(CallbackData, prefix="dynamic_question"):
    action: str
    question_id: str
