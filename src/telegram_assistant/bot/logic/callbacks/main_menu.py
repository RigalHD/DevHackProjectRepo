from aiogram import F, Router
from aiogram.types import CallbackQuery

from telegram_assistant.bot.logic.callbackdata import MainMenuCBData
from telegram_assistant.bot.logic.callbackdata.main_menu_cb_data import QuestionCBData
from telegram_assistant.bot.logic.keyboards.inline import main_menu_kb
from telegram_assistant.llm.llm_repo import LLMRepository
from telegram_assistant.llm.yandex_gpt import YandexGPT

router = Router()


@router.callback_query(MainMenuCBData.filter(F.action == "BackToMainMenu"))
async def back_to_main_menu_handler(query: CallbackQuery) -> None:
    message_text = f"<b>Приветствую, {query.from_user.first_name}</b>\n\n"

    await query.message.edit_text(
        text=message_text,
        reply_markup=main_menu_kb(),
    )
    
@router.callback_query(QuestionCBData.filter(F.action == "Question"))
async def ask_question_handler(query: CallbackQuery, callback_data: QuestionCBData, llm_repo: LLMRepository) -> None:
    question = llm_repo.context_manager.questions_ids[callback_data.question_id]
    message_text = llm_repo.get_question_info(question)
    
    await query.message.answer(
        text=message_text,
    )


@router.callback_query(MainMenuCBData.filter(F.action == "BackToMainMenu"))
async def back_to_main_menu_handler(query: CallbackQuery) -> None:
    message_text = f"<b>Приветствую, {query.from_user.first_name}</b>\n\n"

    await query.message.edit_text(
        text=message_text,
        reply_markup=main_menu_kb(),
    )
