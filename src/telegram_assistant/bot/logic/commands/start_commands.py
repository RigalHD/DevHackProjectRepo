from aiogram import Router
from aiogram.filters import CommandObject, CommandStart
from aiogram.types import Message
from aiogram.utils.deep_linking import decode_payload

from telegram_assistant.bot.logic.keyboards.inline import main_menu_kb
from telegram_assistant.llm.llm_repo import LLMRepository
from telegram_assistant.parser.repository.parser_repo import ParserRepository

router = Router()


@router.message(CommandStart(deep_link=True))
async def start_with_deep_link(
    message: Message,
    command: CommandObject,
    parse_repo: ParserRepository,
    llm_repo: LLMRepository,
) -> None:
    try:
        if args := decode_payload(command.args):
            use_llm = False
            if args.startswith("teacher_"):
                use_llm = True
                url_start = "https://sfedu.ru/s7/person/ru/"
                _id = args.lstrip("teacher_")
                talk_about = "учителе"
                full_url = url_start + _id
                context = parse_repo.base_parser.parse_teacher_info(full_url)
            elif args.startswith("department_"):
                use_llm = True
                url_start = "http://www.mmcs.sfedu.ru/"
                _id = args.lstrip("department_")
                talk_about = "кафедре"
                full_url = url_start + _id
                context = parse_repo.base_parser.parse_department_page(full_url)
            elif args.startswith("place_"):
                use_llm = True
                _id = args.lstrip("place_")
                talk_about = "направлении"
                full_url = "https://sfedu.ru/www/stat_pages22.show?p=ABT/N8206"
                context = str(parse_repo.parse_specific_row(row_number=int(_id)))

            if use_llm:
                await message.answer("Генерация ответа может занять некоторое время...")
                context_addition = (
                    "Максимальная длина твоего ответа - 3000 символов."
                    " На айди вопроса не обращай внимание!"
                    "Если вдруг, исходя ТОЛЬКО ИЗ КОНТЕКСТА, информации нет вообще никакой,"
                    f"то ты должен дать в ответе извиниться и дать эту ссылку: {full_url}"
                )
                info = llm_repo.get_dynamic_question_info(
                    question=f"Расскажи об этом {talk_about} вкратце, ID={_id}",
                    context=context + context_addition,
                )

                await message.answer(text=info)

    except:
        await message.answer("К сожалению, у нас отсутствует информация или данные некорректны")


@router.message(CommandStart())
async def start(message: Message) -> None:
    message_text = (
        f"<b>Приветствую, {message.from_user.first_name}</b>\n"
        "Данный бот сочетает в себе актуальную информацию и ИИ ассистента,"
        "что позволяет пользователю получать краткую и "
        "максимально информативную выжимку данных"
    )

    await message.answer(
        text=message_text,
        reply_markup=main_menu_kb(),
    )
