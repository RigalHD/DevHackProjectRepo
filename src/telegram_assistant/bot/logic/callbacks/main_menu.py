from aiogram import F, Router
from aiogram.types import CallbackQuery
from aiogram.utils.deep_linking import create_start_link

from telegram_assistant.bot.logic.callbackdata import MainMenuCBData
from telegram_assistant.bot.logic.callbackdata.main_menu_cb_data import ParseCBData, QuestionCBData
from telegram_assistant.bot.logic.keyboards.inline import main_menu_kb
from telegram_assistant.llm.llm_repo import LLMRepository
from telegram_assistant.parser.repository.parser_repo import ParserRepository


router = Router()

MAX_MESSAGE_LEN = 4000


@router.callback_query(MainMenuCBData.filter(F.action == "BackToMainMenu"))
async def back_to_main_menu_handler(query: CallbackQuery) -> None:
    message_text = f"<b>Приветствую, {query.from_user.first_name}</b>\n\n"

    await query.message.edit_text(
        text=message_text,
        reply_markup=main_menu_kb(),
    )


@router.callback_query(QuestionCBData.filter(F.action == "Question"))
async def ask_question_handler(query: CallbackQuery, callback_data: QuestionCBData, llm_repo: LLMRepository) -> None:
    await query.message.answer(
        text="Генерация ответа может занять некоторое время...",
        parse_mode="HTML",
    )
    message_text = llm_repo.get_question_info(callback_data.question_id)
    await query.message.answer(
        text=message_text,
        parse_mode="HTML",
    )


@router.callback_query(ParseCBData.filter(F.action == "TeachersParse"))
async def teachers_parse_handler(query: CallbackQuery, parse_repo: ParserRepository) -> None:
    message_texts: list[str] = [""]
    teachers_dict = parse_repo.url_parser.parse_teachers()
    
    for teacher_name, teacher_url in teachers_dict.items():
        cutted_teacher_url = "teacher_" + teacher_url.split("/")[-1]
        try:
            deep_link = await create_start_link(query.bot, cutted_teacher_url, encode=True)
        except:
            continue
        teacher_info = f'<a href="{deep_link}">{teacher_name}</a>\n'
        if len(message_texts[-1] + teacher_info) > MAX_MESSAGE_LEN:
            message_texts.append(teacher_info)
        else:
            message_texts[-1] += teacher_info

    for text in message_texts:
        await query.message.answer(
            text=text,
            parse_mode="HTML",
        )
    
    await query.message.answer(
        text="Нажмите на ФИО любого учителя, чтобы получить краткий рассказ о нем"
    )
