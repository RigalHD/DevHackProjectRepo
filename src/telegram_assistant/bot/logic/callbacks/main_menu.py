from aiogram import F, Router
from aiogram.types import CallbackQuery
from aiogram.utils.deep_linking import create_start_link

from telegram_assistant.bot.logic.callbackdata import MainMenuCBData
from telegram_assistant.bot.logic.callbackdata.main_menu_cb_data import ParseCBData, QuestionCBData
from telegram_assistant.llm.llm_repo import LLMRepository
from telegram_assistant.parser.repository.parser_repo import ParserRepository

router = Router()

MAX_MESSAGE_LEN = 4000


@router.callback_query(MainMenuCBData.filter(F.action == "ScheduleURL"))
async def schedule_url_handler(query: CallbackQuery) -> None:
    message_text = "<b>Точное расписание можно узнать здесь:</b>\n" + "http://www.mmcs.sfedu.ru/timetable"

    await query.message.answer(message_text)


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

    await query.message.answer(text="Нажмите на ФИО любого учителя, чтобы получить краткий рассказ о нем")


@router.callback_query(ParseCBData.filter(F.action == "PlacesParse"))
async def places_parse_handler(query: CallbackQuery, parse_repo: ParserRepository) -> None:
    message_texts: list[str] = [""]
    places_dict = parse_repo.parse_table(reversed_result=False)

    for row, name in places_dict.items():
        cutted_place_url = "place_" + row.lstrip("row")
        deep_link = await create_start_link(query.bot, cutted_place_url, encode=True)
        place_info = f'<a href="{deep_link}">{name}</a>\n'
        if len(message_texts[-1] + place_info) > MAX_MESSAGE_LEN:
            message_texts.append(place_info)
        else:
            message_texts[-1] += place_info

    for text in message_texts:
        await query.message.answer(
            text=text,
            parse_mode="HTML",
        )

    await query.message.answer(text="Нажмите на название направления, чтобы получить краткий рассказ о нем")


@router.callback_query(ParseCBData.filter(F.action == "DepartmentsParse"))
async def department_parse_handler(query: CallbackQuery, parse_repo: ParserRepository) -> None:
    message_texts: list[str] = [""]
    departments_dict = parse_repo.url_parser.parse_departments()

    for department_name, department_url in departments_dict.items():
        cutted_department_url = "department_" + department_url.lstrip("http://www.mmcs.sfedu.ru/").lstrip(
            "http://www.mmcs.sfedu.ru/21-2009-02-18-12-38-00",
        )

        try:
            deep_link = await create_start_link(query.bot, cutted_department_url, encode=True)
        except:
            continue
        department_info = f'<a href="{deep_link}">{department_name}</a>\n'
        if len(message_texts[-1] + department_info) > MAX_MESSAGE_LEN:
            message_texts.append(department_info)
        else:
            message_texts[-1] += department_info

    for text in message_texts:
        await query.message.answer(
            text=text,
            parse_mode="HTML",
        )

    await query.message.answer(text="Чтобы узнать о кафедре больше, Вам нужно нажать на ее название")
